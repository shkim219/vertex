package kmeans;

import com.opencsv.CSVWriter;
import org.apache.ignite.Ignite;
import org.apache.ignite.IgniteCache;
import org.apache.ignite.Ignition;
import org.apache.ignite.cache.affinity.rendezvous.RendezvousAffinityFunction;
import org.apache.ignite.cache.query.QueryCursor;
import org.apache.ignite.cache.query.ScanQuery;
import org.apache.ignite.configuration.CacheConfiguration;
import org.apache.ignite.configuration.IgniteConfiguration;
import org.apache.ignite.ml.clustering.kmeans.KMeansModel;
import org.apache.ignite.ml.clustering.kmeans.KMeansTrainer;
import org.apache.ignite.ml.dataset.feature.extractor.Vectorizer;
import org.apache.ignite.ml.dataset.feature.extractor.impl.DummyVectorizer;
import org.apache.ignite.ml.math.Tracer;
import org.apache.ignite.ml.math.primitives.vector.Vector;
import org.apache.ignite.ml.math.primitives.vector.VectorUtils;

import javax.cache.Cache;
import java.io.*;
import java.lang.reflect.Array;
import java.util.*;
import graphql.Fetch;

public class Client {
    private static ArrayList<String> ids = new ArrayList<String>();
    private static double firstData = 0.0;
    private static int numFirstData;
    private static ArrayList<String> dataFile = new ArrayList<String>();
    private static String[] headers;
    public static void main(String args[]) throws IOException, InterruptedException {
//        String filename = args[0];
//        String pathname = args[1];
//        System.out.println(filename);
//        System.out.println(pathname);
        String filename = "features.csv";
//        ArrayList<String> fetched = Fetch.fetch(filename, pathname);
        ArrayList<String> fetched = fetch(filename, "/home/kimse/vertex/shkim219/query/__init__.py");
        IgniteConfiguration configuration = new IgniteConfiguration();
        configuration.setClientMode(false);

        try (Ignite ignite = Ignition.start(configuration)) {
            IgniteCache<Integer, Vector> data = getCache(ignite, "ENTRY");

            getData(fetched, data); //change csv

            //int numClusters = ids.size() * numFirstData; //change to getting clusters from hypi
            int numClusters = ask(ids.size());


            Vectorizer<Integer, Vector, Integer, Double> vectorizer =
                    new DummyVectorizer<Integer>().labeled(Vectorizer.LabelCoordinate.FIRST);

            KMeansTrainer trainer = new KMeansTrainer().withAmountOfClusters(numClusters);
            KMeansModel mdl = trainer.fit(ignite, data, vectorizer);

            for(int i = 0; i < numClusters; i++)
                Tracer.showAscii(mdl.centers()[i]);

            try (QueryCursor<Cache.Entry<Integer, Vector>> observations = data.query(new ScanQuery<>())) {
                int[] numpred = new int[numClusters];
                //int[] numreal = new int[numClusters];
                ArrayList<Entry> vectorpred = new ArrayList<>();
                for (Cache.Entry<Integer, Vector> observation : observations) {
                    Vector val = observation.getValue();
                    Vector inputs = val.copyOfRange(1, val.size());
                    //double real = val.get(0);
                    //numreal[(int)(real)]++;
                    double prediction = mdl.predict(inputs);
                    numpred[(int)(prediction)]++;
                    vectorpred.add(new Entry((int)(prediction),val));

                    //System.out.printf(">>> | %.4f\t\t\t| %.4f\t\t|\n", prediction, groundTruth);
                }
//                System.out.println(Arrays.toString(numpred));
//                System.out.println(Arrays.toString(numreal));
                double sd = askSD();
                getOutliers(mdl.centers(), vectorpred, filename, numpred, sd); //change csv
            }
            finally {
                if (data != null)
                    data.destroy();
            }
        }
        System.out.flush();
    }

    private static ArrayList<String> fetch(String filename, String pathname) throws IOException, InterruptedException {
        ProcessBuilder pb = new ProcessBuilder("python", pathname, filename);//.inheritIO();
//        ProcessBuilder pb = new ProcessBuilder("python", path).inheritIO();
        Process p = pb.start();
        BufferedReader bfr = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String line = "";
        ArrayList<String> fetched = new ArrayList<String>();
        int count = 0;
        while ((line = bfr.readLine()) != null){
//            System.out.println(line);
            //count++;
            fetched.add(line);
        }
        //System.out.println(count);
        p.waitFor();
        return fetched;

    }

    private static double askSD() throws IOException{
        Scanner sc = new Scanner(System.in);
        System.out.println("z = 2 is standard for finding outliers. Proceed or use custom? [Y/Custom]");
        String response1 = sc.nextLine().toUpperCase();
        if(!response1.equals("Y")){
            System.out.println("What threshold?");
            String response2 = sc.nextLine();
            try {
                double ret = Double.parseDouble(response2);
                if (ret <= 0){
                    System.out.println("Clusters more than 0 is needed");
                    return askSD();
                }
                return ret;
            }
            catch (NumberFormatException e){
                System.out.println("Incorrect format, only put integer");
                return askSD();
            }
        }
        return 2.0;
    }

    private static int ask(int numClusters) throws IOException{
        Scanner sc = new Scanner(System.in);
        System.out.println(numClusters + " of images found. Proceed or use custom? [Y/Custom] Default: Custom");
        String response1 = sc.nextLine().toUpperCase();
        if(!response1.equals("Y")){
            System.out.println("How many clusters?");
            String response2 = sc.nextLine();
            try {
                int ret = Integer.parseInt(response2);
                return ret;
            }
            catch (NumberFormatException e){
                System.out.println("Incorrect format, only put integer");
                return ask(numClusters);
            }
        }
        return numClusters;
    }

    private static void getData(ArrayList<String> file, IgniteCache<Integer, Vector> cache) throws FileNotFoundException {
        int cnt = 0;
        for (String row : file) {
            row = row.substring(1, row.length() - 1);
            dataFile.add(row);
            String[] cells = row.split(",");
            double[] features = new double[cells.length];

            for (int j = 0; j < cells.length - 1; j++)
                if (!cells[j].contains("None"))
                    features[j + 1] = Double.parseDouble(cells[j]);
            double id = getID(cells[cells.length - 1]);
            features[0] = id;

            //addFirst(features[1]);

            cache.put(cnt++, VectorUtils.of(features));
        }
    }

    private static void getOutliers(Vector[] centers, ArrayList<Entry> vectors, String filename, int[] predict, double sd) throws IOException {
        File file = new File(filename.substring(0,filename.indexOf(".csv")) + "outliers.csv");
        try {
            FileWriter out = new FileWriter(file);
            CSVWriter writer = new CSVWriter(out);
            writer.writeNext(headers);
            //Vector[] avg = new Vector[centers.length];
            double[][] avg = new double[centers.length][vectors.get(0).getData().size() - 1];
            ArrayList<Integer> outliers = new ArrayList<Integer>();
            ArrayList<Double> distances = new ArrayList<Double>();
            for (int i = 0; i < vectors.size(); i++) {
                int predicted = vectors.get(i).getPredict();
                Vector curVector = vectors.get(i).getData();
                int curVectorSize = curVector.size() - 1;
                Vector curCenter = centers[predicted];
                double sum = 0;
                for (int j = 0; j < curVectorSize; j++) {
                    double curDistance = Math.abs(curCenter.get(j) - curVector.get(j + 1));
                        avg[predicted][j] += curDistance;
                    sum += curDistance * curDistance;
                }
                sum = Math.pow(sum, 1.0/curVectorSize);
                distances.add(sum);
            }
            double[] averageDistances = new double[avg.length];
            for (int i = 0; i < avg.length; i++) {
                int predictCur = predict[i];
                double sum = 0;
                for (int j = 0; j < avg[i].length; j++){
                    avg[i][j] /= predictCur;
                    sum += avg[i][j];
                }
                sum = Math.pow(sum, 1.0/avg[i].length);
                averageDistances[i] = sum;
            }
            double[] standardDeviations = new double[avg.length];
            for (int i = 0; i < vectors.size(); i++) {
                int predicted = vectors.get(i).getPredict();
                double averageCompare = averageDistances[predicted];
                double predictedDistance = distances.get(i);
                standardDeviations[predicted] += Math.pow(averageCompare - predictedDistance, 2);
            }
            for (int i = 0; i < standardDeviations.length; i++) {
                standardDeviations[i] /= predict[i];
                standardDeviations[i] = Math.pow(standardDeviations[i], 0.5);
            }
            int countOfOutliers = 0;
            for (int i = 0; i < vectors.size(); i++) {
                Vector curVector = vectors.get(i).getData();
                int predicted = vectors.get(i).getPredict();
                double averageCompare = averageDistances[predicted];
                double standardDeviation = standardDeviations[predicted];
                double predictedDistance = distances.get(i);
                if((predictedDistance - averageCompare)/standardDeviation >= sd) {
                    String[] valueOfVector = new String[curVector.size()];
                    valueOfVector[valueOfVector.length - 1] = ids.get((int)(curVector.get(0)));
                    double[] othervalues = vectors.get(i).getData().copyOfRange(1, vectors.get(i).getData().size()).asArray();
                    for (int k = 0; k < othervalues.length; k++) {
                        valueOfVector[k] = Double.toString(othervalues[k]);
                    }
                    writer.writeNext(valueOfVector);
                    countOfOutliers++;
                }
            }
            if (countOfOutliers == 0){
                System.out.println("No outliers found");
            }
            else{
                System.out.println(countOfOutliers + " outliers found");
            }
            writer.close();
        }
        catch (IOException e){
            e.printStackTrace();
        }
    }

    private static IgniteCache<Integer, Vector> getCache(Ignite ignite, String nameOfCache){
        CacheConfiguration<Integer, Vector> cacheConfiguration = new CacheConfiguration<>();
        cacheConfiguration.setName(nameOfCache);
        cacheConfiguration.setAffinity(new RendezvousAffinityFunction(false, 10));

        return ignite.createCache(cacheConfiguration);

    }
    private static double getID(String id){
        for (int i = 0; i < ids.size(); i++) {
            if (id.equals(ids.get(i))) {
                return Double.valueOf(i);
            }
        }
        ids.add(id);
        return ids.size() - 1.0;
    }

    private static void addFirst(double datum){
        if(firstData == 0.0) {
            firstData = datum;
            numFirstData++;
        }
        else if(datum == firstData)
            numFirstData++;
    }

    private static class Entry {
        private final Vector data;
        private final int predict;

        public Entry(int predict, Vector data){
            this.data = data;
            this.predict = predict;
        }
        public Vector getData(){
            return data;
        }
        public int getPredict(){
            return predict;
        }
    }
}

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
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Array;
import java.util.*;

public class Client {
    private static ArrayList<String> ids = new ArrayList<String>();
    private static double firstData = 0.0;
    private static int numFirstData;
    private static ArrayList<String> dataFile = new ArrayList<String>();
    private static String[] headers;
    public static void main(String... args) throws IOException {
        IgniteConfiguration configuration = new IgniteConfiguration();
        configuration.setClientMode(false);

        try (Ignite ignite = Ignition.start(configuration)) {
            IgniteCache<Integer, Vector> data = getCache(ignite, "ENTRY");

            getData("C:\\Users\\paulk\\IdeaProjects\\skopytest\\src\\main\\resources\\skopy.csv", data); //change csv

            //int numClusters = ids.size() * numFirstData; //change to getting clusters from hypi
            int numClusters = ids.size();
            Vectorizer<Integer, Vector, Integer, Double> vectorizer =
                    new DummyVectorizer<Integer>().labeled(Vectorizer.LabelCoordinate.FIRST);

            KMeansTrainer trainer = new KMeansTrainer().withAmountOfClusters(numClusters);
            KMeansModel mdl = trainer.fit(ignite, data, vectorizer);

            for(int i = 0; i < numClusters; i++)
                Tracer.showAscii(mdl.centers()[i]);

            try (QueryCursor<Cache.Entry<Integer, Vector>> observations = data.query(new ScanQuery<>())) {
                int[] numpred = new int[3];
                int[] numreal = new int[3];
                ArrayList<Entry> vectorpred = new ArrayList<>();
                for (Cache.Entry<Integer, Vector> observation : observations) {
                    Vector val = observation.getValue();
                    Vector inputs = val.copyOfRange(1, val.size());
                    double real = val.get(0);
                    numreal[(int)(real)]++;
                    double prediction = mdl.predict(inputs);
                    numpred[(int)(prediction)]++;
                    vectorpred.add(new Entry((int)(prediction),val));

                    //System.out.printf(">>> | %.4f\t\t\t| %.4f\t\t|\n", prediction, groundTruth);
                }
                System.out.println(Arrays.toString(numpred));
                System.out.println(Arrays.toString(numreal));
                getOutliers(numpred, numreal, vectorpred); //change csv
            }
            finally {
                if (data != null)
                    data.destroy();
            }
        }
        System.out.flush();
    }

    private static void getData(String file, IgniteCache<Integer, Vector> cache) throws FileNotFoundException {
        Scanner scanner = new Scanner(new File(file));
        headers = scanner.nextLine().split(",");
        int cnt = 0;
        while (scanner.hasNextLine()) {
            String row = scanner.nextLine();
            dataFile.add(row);
            String[] cells = row.split(",");
            double[] features = new double[cells.length];

            for (int i = 0; i < cells.length - 1; i++)
                if(cells[i] != "")
                    features[i+1] = Double.valueOf(cells[i]);
            double id = getID(cells[cells.length - 1]);
            features[0] = id;

            //addFirst(features[1]);

            cache.put(cnt++, VectorUtils.of(features));
        }
    }

    private static void getOutliers(int[] pred, int[] real, ArrayList<Entry> vectors) throws IOException {
        File file = new File("outliers.csv");
        try {
            FileWriter out = new FileWriter(file);
            CSVWriter writer = new CSVWriter(out);
            writer.writeNext(headers);
            int sum = 0;
            for (int num : real) {
                sum += num;
            }
            ArrayList<Integer> outliers = new ArrayList<Integer>();
            for (int i = 0; i < pred.length; i++) {
                if (pred[i] < (sum * 0.05)) {
                    outliers.add(i);
                }
            }
            for (int i = 0; i < vectors.size(); i++) {
                int predicted = vectors.get(i).getPredict();
                Vector curVector = vectors.get(i).getData();
                for (int j = 0; j < outliers.size(); j++) {
                    if (predicted == outliers.get(j)) {
                        String[] valueOfVector = new String[curVector.size()];
                        valueOfVector[valueOfVector.length - 1] = ids.get((int)(curVector.get(0)));
                        double[] othervalues = vectors.get(i).getData().copyOfRange(1, vectors.get(i).getData().size()).asArray();
                        for (int k = 0; k < othervalues.length; k++) {
                            valueOfVector[k] = Double.toString(othervalues[k]);
                        }
                        writer.writeNext(valueOfVector);
                    }
                }
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

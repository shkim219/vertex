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
    private static String[] headers = {"classification", "ml", "numClusters", "sd", "area", "bounding_box_area", "bounding_box_maximum_column", "bounding_box_maximum_row", "bounding_box_minimum_column", "bounding_box_minimum_row", "centroid_column", "centroid_row", "centroid_weighted_column",
            "centroid_weighted_local_column", "centroid_weighted_local_row", "centroid_weighted_row", "convex_hull_area", "eccentricity", "equivalent_diameter", "euler_number", "extent", "inertia_tensor_0_0", "inertia_tensor_0_1",
            "inertia_tensor_1_0", "inertia_tensor_1_1", "inertia_tensor_eigen_values_0", "inertia_tensor_eigen_values_1", "intensity_integrated", "intensity_maximum", "intensity_mean", "intensity_median", "intensity_median_absolute_deviation",
            "intensity_minimum", "intensity_quartile_1", "intensity_quartile_2", "intensity_quartile_3", "intensity_standard_deviation", "label", "major_axis_length", "minor_axis_length", "moments_central_0_0", "moments_central_0_1",
            "moments_central_0_2", "moments_central_1_0", "moments_central_1_1", "moments_central_1_2", "moments_central_2_0", "moments_central_2_1", "moments_central_2_2", "moments_hu_0", "moments_hu_1", "moments_hu_2", "moments_hu_3",
            "moments_hu_4", "moments_hu_5", "moments_hu_6", "moments_hu_weighted_0", "moments_hu_weighted_1", "moments_hu_weighted_2", "moments_hu_weighted_3", "moments_hu_weighted_4", "moments_hu_weighted_5", "moments_hu_weighted_6",
            "moments_normalized_0_0", "moments_normalized_0_1", "moments_normalized_0_2", "moments_normalized_1_0", "moments_normalized_1_1", "moments_normalized_1_2", "moments_normalized_2_0", "moments_normalized_2_1", "moments_normalized_2_2",
            "moments_spatial_0_0", "moments_spatial_0_1", "moments_spatial_0_2", "moments_spatial_1_0", "moments_spatial_1_1", "moments_spatial_1_2", "moments_spatial_2_0", "moments_spatial_2_1", "moments_spatial_2_2", "moments_weighted_central_0_0",
            "moments_weighted_central_0_1", "moments_weighted_central_0_2", "moments_weighted_central_1_0", "moments_weighted_central_1_1", "moments_weighted_central_1_2", "moments_weighted_central_2_0", "moments_weighted_central_2_1",
            "moments_weighted_central_2_2", "moments_weighted_normalized_0_0", "moments_weighted_normalized_0_1", "moments_weighted_normalized_0_2", "moments_weighted_normalized_1_0", "moments_weighted_normalized_1_1", "moments_weighted_normalized_1_2",
            "moments_weighted_normalized_2_0", "moments_weighted_normalized_2_1", "moments_weighted_normalized_2_2", "moments_weighted_spatial_0_0", "moments_weighted_spatial_0_1", "moments_weighted_spatial_0_2", "moments_weighted_spatial_1_0",
            "moments_weighted_spatial_1_1", "moments_weighted_spatial_1_2", "moments_weighted_spatial_2_0", "moments_weighted_spatial_2_1", "moments_weighted_spatial_2_2", "orientation", "perimeter", "shannon_entropy_hartley", "shannon_entropy_natural",
            "shannon_entropy_shannon", "solidity", "moments_zernike_8_8_00", "moments_zernike_8_8_01", "moments_zernike_8_8_02", "moments_zernike_8_8_03", "moments_zernike_8_8_04", "moments_zernike_8_8_05", "moments_zernike_8_8_06", "moments_zernike_8_8_07",
            "moments_zernike_8_8_08", "moments_zernike_8_8_09", "moments_zernike_8_8_10", "moments_zernike_8_8_11", "moments_zernike_8_8_12", "moments_zernike_8_8_13", "moments_zernike_8_8_14", "moments_zernike_8_8_15", "moments_zernike_8_8_16",
            "moments_zernike_8_8_17", "moments_zernike_8_8_18", "moments_zernike_8_8_19", "moments_zernike_8_8_20", "moments_zernike_8_8_21", "moments_zernike_8_8_22", "moments_zernike_8_8_23", "moments_zernike_8_8_24", "threshold_adjacency_statistics_00",
            "threshold_adjacency_statistics_01", "threshold_adjacency_statistics_02", "threshold_adjacency_statistics_03", "threshold_adjacency_statistics_04", "threshold_adjacency_statistics_05", "threshold_adjacency_statistics_06",
            "threshold_adjacency_statistics_07", "threshold_adjacency_statistics_08", "threshold_adjacency_statistics_09", "threshold_adjacency_statistics_10", "threshold_adjacency_statistics_11", "threshold_adjacency_statistics_12",
            "threshold_adjacency_statistics_13", "threshold_adjacency_statistics_14", "threshold_adjacency_statistics_15", "threshold_adjacency_statistics_16", "threshold_adjacency_statistics_17", "threshold_adjacency_statistics_18",
            "threshold_adjacency_statistics_19", "threshold_adjacency_statistics_20", "threshold_adjacency_statistics_21", "threshold_adjacency_statistics_22", "threshold_adjacency_statistics_23", "threshold_adjacency_statistics_24",
            "threshold_adjacency_statistics_25", "threshold_adjacency_statistics_26", "threshold_adjacency_statistics_27", "threshold_adjacency_statistics_28", "threshold_adjacency_statistics_29", "threshold_adjacency_statistics_30",
            "threshold_adjacency_statistics_31", "threshold_adjacency_statistics_32", "threshold_adjacency_statistics_33", "threshold_adjacency_statistics_34", "threshold_adjacency_statistics_35", "threshold_adjacency_statistics_36",
            "threshold_adjacency_statistics_37", "threshold_adjacency_statistics_38", "threshold_adjacency_statistics_39", "threshold_adjacency_statistics_40", "threshold_adjacency_statistics_41", "threshold_adjacency_statistics_42",
            "threshold_adjacency_statistics_43", "threshold_adjacency_statistics_44", "threshold_adjacency_statistics_45", "threshold_adjacency_statistics_46", "threshold_adjacency_statistics_47", "threshold_adjacency_statistics_48",
            "threshold_adjacency_statistics_49", "threshold_adjacency_statistics_50", "threshold_adjacency_statistics_51", "threshold_adjacency_statistics_52", "threshold_adjacency_statistics_53", "local_binary_patterns_00_08_06",
            "local_binary_patterns_01_08_06", "local_binary_patterns_02_08_06", "local_binary_patterns_03_08_06", "local_binary_patterns_04_08_06", "local_binary_patterns_05_08_06", "local_binary_patterns_06_08_06", "local_binary_patterns_07_08_06",
            "local_binary_patterns_08_08_06", "local_binary_patterns_09_08_06", "local_binary_patterns_10_08_06", "local_binary_patterns_11_08_06", "local_binary_patterns_12_08_06", "local_binary_patterns_13_08_06", "haralick_angular_second_moment_8_000",
            "haralick_contrast_8_000", "haralick_correlation_8_000", "haralick_sum_of_squares_variance_8_000", "haralick_inverse_difference_moment_8_000", "haralick_sum_average_8_000", "haralick_sum_variance_8_000", "haralick_sum_entropy_8_000",
            "haralick_entropy_8_000", "haralick_difference_variance_8_000", "haralick_difference_entropy_8_000", "haralick_information_measure_of_correlation_1_8_000", "haralick_information_measure_of_correlation_2_8_000",
            "haralick_angular_second_moment_8_090", "haralick_contrast_8_090", "haralick_correlation_8_090", "haralick_sum_of_squares_variance_8_090", "haralick_inverse_difference_moment_8_090", "haralick_sum_average_8_090", "haralick_sum_variance_8_090",
            "haralick_sum_entropy_8_090", "haralick_entropy_8_090", "haralick_difference_variance_8_090", "haralick_difference_entropy_8_090", "haralick_information_measure_of_correlation_1_8_090", "haralick_information_measure_of_correlation_2_8_090",
            "haralick_angular_second_moment_8_180", "haralick_contrast_8_180", "haralick_correlation_8_180", "haralick_sum_of_squares_variance_8_180", "haralick_inverse_difference_moment_8_180", "haralick_sum_average_8_180", "haralick_sum_variance_8_180",
            "haralick_sum_entropy_8_180", "haralick_entropy_8_180", "haralick_difference_variance_8_180", "haralick_difference_entropy_8_180", "haralick_information_measure_of_correlation_1_8_180", "haralick_information_measure_of_correlation_2_8_180",
            "haralick_angular_second_moment_8_270", "haralick_contrast_8_270", "haralick_correlation_8_270", "haralick_sum_of_squares_variance_8_270", "haralick_inverse_difference_moment_8_270", "haralick_sum_average_8_270", "haralick_sum_variance_8_270",
            "haralick_sum_entropy_8_270", "haralick_entropy_8_270", "haralick_difference_variance_8_270", "haralick_difference_entropy_8_270", "haralick_information_measure_of_correlation_1_8_270", "haralick_information_measure_of_correlation_2_8_270",
            "pathname"};
    public static void main(String args[]) throws IOException, InterruptedException {
        String filename = args[0];
//        String testname = args[1];
//        System.out.println(filename);
//        String filename = "data.csv";
//        String testname = "data.csv";
//        ArrayList<String> fetched = Fetch.fetch(filename, pathname);
        ArrayList<String> fetched = new ArrayList<>();
//        ArrayList<String> fetchedTest = new ArrayList<>();
        if(Fetch.fetch(filename).size() == 0) {
            try {
                fetched = Fetch.fetch2(filename);
            }
            catch (FileNotFoundException e){
                System.out.println("cannot find the file");
                System.exit(0);
            }
        }
        else
            fetched = Fetch.fetch(filename);

        IgniteConfiguration configuration = new IgniteConfiguration();
        configuration.setClientMode(false);

        try (Ignite ignite = Ignition.start(configuration)) {
            IgniteCache<Integer, Vector> data = getCache(ignite, "ENTRY");

            getData(fetched, data); //change csv

//            int numClusters = ids.size() * numFirstData; //change to getting clusters from hypi
            int numClusters = ask(ids.size());
//            int numClusters = 2;

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
                File file = new File(filename.substring(0,filename.indexOf(".csv")) + "predictedkmeans.csv");
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
                getOutliers(mdl.centers(), vectorpred, filename, numpred, sd);
            }
            finally {
                if (data != null)
                    data.destroy();
            }
        }
        System.out.flush();
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
            row = row.substring(0, row.length()); //change to 1 and -1
            dataFile.add(row);
            String[] cells = row.split(",");
            double[] features = new double[cells.length - 1];

            for (int j = 0; j < cells.length - 1; j++)
                if (!cells[j].equals("") && !cells[j].contains("None"))//
                    features[j] = Double.parseDouble(cells[j]);
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
            String[] kmeansArr = {Integer.toString(centers.length), Double.toString(sd)};
//            writer.writeNext(kmeansArr);
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
                    String[] valueOfVector = new String[curVector.size() + 4];
                    valueOfVector[valueOfVector.length - 1] = ids.get((int)(curVector.get(0)));
                    double[] othervalues = vectors.get(i).getData().copyOfRange(1, vectors.get(i).getData().size()).asArray();
                    for (int k = 0; k < othervalues.length; k++) {
                        valueOfVector[k + 3] = Double.toString(othervalues[k]);
                    }
                    valueOfVector[0] = "-1";
                    valueOfVector[1] = "kmeans";
                    valueOfVector[2] = Integer.toString(centers.length);
                    valueOfVector[3] = Double.toString(sd);
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

package randomforest;

import com.opencsv.CSVWriter;
import graphql.Fetch;
import org.apache.commons.math3.util.Precision;
import org.apache.ignite.Ignite;
import org.apache.ignite.IgniteCache;
import org.apache.ignite.Ignition;
import org.apache.ignite.cache.affinity.rendezvous.RendezvousAffinityFunction;

import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.WeakHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import org.apache.ignite.cache.query.Query;
import org.apache.ignite.cache.query.QueryCursor;
import org.apache.ignite.cache.query.ScanQuery;
import org.apache.ignite.configuration.CacheConfiguration;
import org.apache.ignite.configuration.IgniteConfiguration;
import org.apache.ignite.ml.composition.ModelsComposition;
import org.apache.ignite.ml.dataset.feature.extractor.Vectorizer;
import org.apache.ignite.ml.dataset.feature.extractor.impl.DummyVectorizer;
import org.apache.ignite.ml.environment.parallelism.ParallelismStrategy;
import org.apache.ignite.ml.math.primitives.vector.Vector;
import org.apache.ignite.ml.tree.randomforest.RandomForestRegressionTrainer;
import org.apache.ignite.ml.dataset.feature.FeatureMeta;
import org.apache.ignite.ml.tree.randomforest.data.FeaturesCountSelectionStrategies;
import org.apache.ignite.ml.environment.LearningEnvironmentBuilder;
import org.apache.ignite.ml.environment.logging.ConsoleLogger;
import org.apache.ignite.ml.math.distances.EuclideanDistance;

import javax.cache.Cache;
import java.util.Scanner;
import org.apache.ignite.ml.math.primitives.vector.VectorUtils;
import graphql.Fetch;

public class Client {
    private static ArrayList<String> ids = new ArrayList<String>();
    private static double firstData = 0.0;
    private static int numFirstData;
    private static ArrayList<String> dataFile = new ArrayList<String>();
    private static String obj;
    private static String[] headers = {"area", "bounding_box_area", "bounding_box_maximum_column", "bounding_box_maximum_row", "bounding_box_minimum_column", "bounding_box_minimum_row", "centroid_column", "centroid_row", "centroid_weighted_column",
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
    public static void main(String... args) throws FileNotFoundException, IOException, InterruptedException {
        String filename = args[0];
//        String pathname = args[1];
//        String filename = "feastures.csv";
//        ArrayList<String> fetched = Fetch.fetch(filename, pathname);

        ArrayList<String> fetched = new ArrayList<>();
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
            //CSVWriter writer = new CSVWriter(new FileWriter("testNOW.csv"));
            IgniteCache<Integer, Vector> data = getCache(ignite, "ENTRY");

            int[] whatToPredict = ask();

            int count = 0;
            double averageError = 0;
            int totalAmount = 0;
            double[] averageErrors = new double[whatToPredict[1] - whatToPredict[0] + 1];
            ArrayList<ArrayList<Double>> predicted = new ArrayList<ArrayList<Double>>(averageErrors.length);

            for (int i = whatToPredict[0]; i <= whatToPredict[1]; i++){

                getData(fetched, data, i);
                AtomicInteger idx = new AtomicInteger(0);
                RandomForestRegressionTrainer trainer = new RandomForestRegressionTrainer(IntStream.range(0, data.get(1).size() - 1).mapToObj(
                        x -> new FeatureMeta("", idx.getAndIncrement(), false)).collect(Collectors.toList())
                ).withAmountOfTrees(5)
                        .withFeaturesCountSelectionStrgy(FeaturesCountSelectionStrategies.ALL)
                        .withMaxDepth(5)
                        .withMinImpurityDelta(0.)
                        .withSubSampleSize(0.7)
                        .withSeed(0);
                trainer.withEnvironmentBuilder(LearningEnvironmentBuilder.defaultBuilder()
                        .withParallelismStrategyTypeDependency(ParallelismStrategy.ON_DEFAULT_POOL)
                        .withLoggingFactoryDependency(ConsoleLogger.Factory.LOW)
                );

                Vectorizer<Integer, Vector, Integer, Double> vectorizer = new DummyVectorizer<Integer>()
                        .labeled(Vectorizer.LabelCoordinate.FIRST);
                ModelsComposition randomForestMdl = trainer.fit(ignite, data, vectorizer);


                try (QueryCursor<Cache.Entry<Integer, Vector>> observations = data.query(new ScanQuery<>())) {
                    for (Cache.Entry<Integer, Vector> observation : observations) {
                        Vector val = observation.getValue();
                        Vector inputs = val.copyOfRange(1, val.size());
                        double groundTruth = val.get(0);

                        double prediction = randomForestMdl.predict(inputs);
                        if(predicted.size()  == count)
                            predicted.add(new ArrayList<Double>());
                        predicted.get(count).add(prediction);
                        double error;
                        if(groundTruth == 0){
                            error = prediction / 100;
                        }
                        else{
                            error = (prediction - groundTruth) / groundTruth;
                        }
                        averageErrors[count] += error;

                        totalAmount++;
                    }

                    //                System.out.println("\n>>> Accuracy " + (1 - amountOfErrors / (double)totalAmount));
                    /*System.out.println(
                            ">>> Random Forest multi-class classification algorithm over cached dataset usage example completed."
                    );*/
                }
                data.clear();

                        /*for (int h = 0; h < 25; h++){
                            averageAverageVariance += (averageAverageError - variance[h]) * (averageAverageError - variance[h]);
                        }
                        averageAverageVariance /= 24;*/
    //                    long stopTime = System.currentTimeMillis();
    //                    String timeTaken = Double.toString((stopTime - startTime)/25000.0);
    //                    System.out.println(i + " with " + timeTaken + " time took for " + Double.toString(averageAverageError));
    //                    writer.writeNext(new String[]{Integer.toString(i), timeTaken , Double.toString(averageAverageError)});

                //writer.close();
                    count++;
            }
            for (int i = 0; i < averageErrors.length; i++) {
                averageErrors[i] /= ((totalAmount * 1.0) / averageErrors.length);
                averageError += averageErrors[i];
            }
            System.out.println("\n>>> Error Averages: " + Arrays.toString(averageErrors) + " on " + (totalAmount/averageErrors.length) + " number of data");
            System.out.println("\n>>> Combined Error Average: " + averageError + " on " + averageErrors.length + " number of features on " + totalAmount + " number of data");
            write(predicted, whatToPredict, fetched, averageError, filename);
            data.destroy();
        }

        System.out.flush();
    }

    private static void write(ArrayList<ArrayList<Double>> predicted, int[] whatToPredict, ArrayList<String> fetched, double error, String filename){
        File file = new File(filename.substring(0,filename.indexOf(".csv")) + "predicted.csv");
        try{
            FileWriter out = new FileWriter(file);
            CSVWriter writer = new CSVWriter(out);
            writer.writeNext(headers);
            String[] nextLine = {obj, Double.toString(error)};
            writer.writeNext(nextLine);
            int count = 0;
            for (String row : fetched) {
                String[] cells = row.split(",");
                for(int i = whatToPredict[0]; i <= whatToPredict[1]; i++) {
                    cells[i] = Double.toString(predicted.get((i - whatToPredict[0])).get(count));
                }
                writer.writeNext(cells);
                count++;
            }
            writer.close();
        }
        catch (IOException e){
            e.printStackTrace();
        }
    }

    private static int[] ask() throws IOException{
        Scanner sc = new Scanner(System.in);
        String[] arrOfPossibleObjects ={"area","bound","centroid","convex hull area","eccentricity","equivalent diameter","extent","inertia","intensity","label","major axis","minor axis","moments","orientation"
                ,"perimeter","shannon entropy","solidity","moments zernike","threshold adjacency statistics","haralick"};

        int[] ranges = {0,0,1,5,6,11,12,12,13,13,14,14,15,15,16,16,17,22,23,32,33,33,34,34,35,35,36,103,104,104,105,105,106,108,109,109,110,134,135,188,189,202,203,254};
        System.out.println("What to predict on? Type number associated with category or name of category");
        for (int i = 0; i < arrOfPossibleObjects.length; i++){
            System.out.println((i+1) + ". " + arrOfPossibleObjects[i]);
        }

        String response1 = sc.nextLine();
        try{
            int response1IntOriginal = Integer.parseInt(response1);
            int response1Int = (response1IntOriginal - 1) * 2;
            int[] retArr = {ranges[response1Int],ranges[response1Int+1]};
            System.out.println("Analyzing " + arrOfPossibleObjects[response1IntOriginal - 1]);
            obj = arrOfPossibleObjects[response1IntOriginal - 1];
            return retArr;
        }
        catch (NumberFormatException e){
            for (int i = 0; i < arrOfPossibleObjects.length; i++){
                String curObject = arrOfPossibleObjects[i];
                if(response1.equals(curObject)){
                    int[] retArr = {ranges[i * 2],ranges[i * 2 + 1]};
                    System.out.println("Analyzing " + curObject);
                    obj = curObject;
                    return retArr;
                }
            }
            System.out.println("None of the options matched, please try again");
            return ask();
        }
    }


    private static void getData(ArrayList<String> file, IgniteCache<Integer, Vector> cache, int toCheck) throws FileNotFoundException {
        int cnt = 0;
        for (String row : file) {
            row = row.substring(0, row.length() - 1);
            dataFile.add(row);
            String[] cells = row.split(",");
            double[] features = new double[cells.length - 1];

            for (int j = 1; j < toCheck; j++)
                if (!cells[j].equals("") && !cells[j].contains("None"))
                    features[j] = Double.parseDouble(cells[j]);
            for (int j = toCheck + 1; j < features.length; j++)
                if (!cells[j].equals("") && !cells[j].contains("None"))
                    features[j] = Double.parseDouble(cells[j]);
            features[0] = Double.parseDouble(cells[toCheck]);
            /*double id = getID(cells[cells.length - 1]);
            features[0] = id;*/

            //addFirst(features[1]);

            cache.put(cnt++, VectorUtils.of(features));
        }
    }
    private static IgniteCache<Integer, Vector> getCache(Ignite ignite, String cachename){
        CacheConfiguration<Integer, Vector> cacheConfiguration = new CacheConfiguration<>();
        cacheConfiguration.setName(cachename);
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

    private static class Entry {
        private final double[] data;
        private final String id;

        public Entry(double[] data, String id){
            this.data = data;
            this.id = id;
        }

        public int size() {
            return data.length;
        }
    }
}


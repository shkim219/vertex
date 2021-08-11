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
    private static String[] headers;
    public static void main(String... args) throws FileNotFoundException, IOException, InterruptedException {
        String filename = args[0];
//        String pathname = args[1];
//        String filename = "features.csv";
//        ArrayList<String> fetched = Fetch.fetch(filename, pathname);
        ArrayList<String> fetched = Fetch.fetch(filename);
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
            data.destroy();
        }

        System.out.flush();
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
            return retArr;
        }
        catch (NumberFormatException e){
            for (int i = 0; i < arrOfPossibleObjects.length; i++){
                String curObject = arrOfPossibleObjects[i];
                if(response1.equals(curObject)){
                    int[] retArr = {ranges[i * 2],ranges[i * 2 + 1]};
                    System.out.println("Analyzing " + curObject);
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
                if (!cells[j].equals(""))//!cells[j].contains("None"))
                    features[j] = Double.parseDouble(cells[j]);
            for (int j = toCheck + 1; j < features.length; j++)
                if (!cells[j].equals(""))//!cells[j].contains("None"))
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


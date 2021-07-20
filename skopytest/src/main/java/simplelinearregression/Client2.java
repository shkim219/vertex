package simplelinearregression;

import org.apache.commons.math3.util.Precision;
import org.apache.ignite.Ignite;
import org.apache.ignite.IgniteCache;
import org.apache.ignite.Ignition;
import org.apache.ignite.cache.affinity.rendezvous.RendezvousAffinityFunction;
import org.apache.ignite.cache.query.QueryCursor;
import org.apache.ignite.cache.query.ScanQuery;
import org.apache.ignite.configuration.CacheConfiguration;
import org.apache.ignite.configuration.IgniteConfiguration;
import org.apache.ignite.ml.composition.ModelsComposition;
import org.apache.ignite.ml.dataset.feature.FeatureMeta;
import org.apache.ignite.ml.dataset.feature.extractor.Vectorizer;
import org.apache.ignite.ml.dataset.feature.extractor.impl.DummyVectorizer;
import org.apache.ignite.ml.environment.LearningEnvironmentBuilder;
import org.apache.ignite.ml.environment.logging.ConsoleLogger;
import org.apache.ignite.ml.environment.parallelism.ParallelismStrategy;
import org.apache.ignite.ml.math.primitives.vector.Vector;
import org.apache.ignite.ml.math.primitives.vector.VectorUtils;
import org.apache.ignite.ml.regressions.linear.LinearRegressionLSQRTrainer;
import org.apache.ignite.ml.regressions.linear.LinearRegressionModel;
import org.apache.ignite.ml.selection.scoring.evaluator.Evaluator;
import org.apache.ignite.ml.selection.scoring.metric.MetricName;
import org.apache.ignite.ml.tree.randomforest.RandomForestRegressionTrainer;
import org.apache.ignite.ml.tree.randomforest.data.FeaturesCountSelectionStrategies;

import javax.cache.Cache;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Client2 {
    public static void main(String... args) throws FileNotFoundException {
        IgniteConfiguration configuration = new IgniteConfiguration();
        configuration.setClientMode(false);

        try (Ignite ignite = Ignition.start(configuration)) {
            IgniteCache<Integer, Vector> data = getCache(ignite, "ENTRY");

            getData("C:\\Users\\paulk\\IdeaProjects\\skopytest\\src\\main\\resources\\skopy.csv",data);
            AtomicInteger idx = new AtomicInteger(0);
            LinearRegressionLSQRTrainer trainer = new LinearRegressionLSQRTrainer();

            System.out.println(">>> Configured trainer: " + trainer.getClass().getSimpleName());
            Vectorizer<Integer, Vector, Integer, Double> vectorizer = new DummyVectorizer<Integer>()
                    .labeled(Vectorizer.LabelCoordinate.FIRST);
            LinearRegressionModel lmdl = trainer.fit(ignite, data, vectorizer);
            double rmse = Evaluator.evaluate(data, lmdl, new DummyVectorizer<Integer>().labeled(Vectorizer.LabelCoordinate.FIRST), MetricName.RMSE);
            System.out.println("\nRMSE: " + rmse);
            /*try (QueryCursor<Cache.Entry<Integer, Vector>> observations = data.query(new ScanQuery<>())){
                for (Cache.Entry<Integer, Vector> observation: observations) {
                    Vector val = observation.getValue();
                    Vector inputs = val.copyOfRange(1, val.size());
                    double groundTruth = val.get(0);

                    double prediction = randomForestMdl.predict(inputs);
                    totalAmount++;
                    if (!Precision.equals(groundTruth, prediction, Precision.EPSILON))
                        amountOfErrors++;
                }
                System.out.println("\n>>> Evaluated model on " + totalAmount + " data points.");

                System.out.println("\n>>> Absolute amount of errors " + amountOfErrors);
                System.out.println("\n>>> Accuracy " + (1 - amountOfErrors / (double)totalAmount));
                System.out.println(
                        ">>> Random Forest multi-class classification algorithm over cached dataset usage example completed."
                );
            }
            finally {
                if (data != null)
                    data.destroy();
            }*/

        }
        System.out.flush();

    }
    private static void getData(String file, IgniteCache<Integer, Vector> cache) throws FileNotFoundException {
        Scanner scanner = new Scanner(new File(file));
        scanner.nextLine();
        int cnt = 0;
        while (scanner.hasNextLine()) {
            String row = scanner.nextLine();
            String[] cells = row.split(",");
            double[] features = new double[cells.length - 1];

            for (int i = 0; i < cells.length - 1; i++)
                if(cells[i] != "")
                    features[i] = Double.valueOf(cells[i]);
            String id = cells[cells.length - 1];

            cache.put(cnt++, VectorUtils.of(features));
        }
    }
    private static IgniteCache<Integer, Vector> getCache(Ignite ignite, String cachename){
        CacheConfiguration<Integer, Vector> cacheConfiguration = new CacheConfiguration<>();
        cacheConfiguration.setName(cachename);
        cacheConfiguration.setAffinity(new RendezvousAffinityFunction(false, 10));

        return ignite.createCache(cacheConfiguration);

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

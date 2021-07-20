package simplelinearregression;

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
import org.apache.ignite.ml.trainers.DatasetTrainer;
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

public class Client {
    public static void main(String... args) throws FileNotFoundException {
        IgniteConfiguration configuration = new IgniteConfiguration();
        configuration.setClientMode(false);

        try (Ignite ignite = Ignition.start(configuration)) {
            IgniteCache<Integer, EntryData> data = getCache(ignite, "EntryData");

            getData("C:\\Users\\paulk\\IdeaProjects\\skopytest\\src\\main\\resources\\skopy.csv",data);
            DatasetTrainer<LinearRegressionModel, Double> trainer = new LinearRegressionLSQRTrainer();

            System.out.println("Training started");
            LinearRegressionModel mdl = trainer.fit(
                    ignite,
                    data,
                    (k, v) -> VectorUtils.of(v.getData()).labeled(Vectorizer.LabelCoordinate.FIRST)
            );
            System.out.println("Training completed");

            try (QueryCursor<Cache.Entry<Integer, EntryData>> cursor = data.query(new ScanQuery<>())) {
                for (Cache.Entry<Integer, EntryData> testEntry : cursor) {
                    EntryData observation = testEntry.getValue();

                    double realPrice = observation.getIntensity();
                    //double predicted = mdl.apply(VectorUtils.of(observation.getData()));
                }
                }

        }

    }
    private static void getData(String file, IgniteCache<Integer, EntryData> cache) throws FileNotFoundException{
        Scanner scanner = new Scanner(new File(file));
        scanner.nextLine();
        int cnt = 0;
        while (scanner.hasNextLine()) {
            String row = scanner.nextLine();
            String[] cells = row.split(",");
            double[] features = new double[cells.length - 1];
            double intensity = 0;

            for (int i = 0; i < cells.length - 1; i++) {
                if(cells[i] != "") {
                    if (i == 25) {
                        intensity = Double.valueOf(cells[i]);
                    }
                    features[i] = Double.valueOf(cells[i]);
                }
            }
            String image = cells[cells.length - 1];

            cache.put(cnt++, new EntryData(features, intensity, image));
        }
    }
    private static IgniteCache<Integer, EntryData> getCache(Ignite ignite, String cachename){
        CacheConfiguration<Integer, EntryData> cacheConfiguration = new CacheConfiguration<>();
        cacheConfiguration.setName(cachename);
        cacheConfiguration.setAffinity(new RendezvousAffinityFunction(false, 10));

        return ignite.createCache(cacheConfiguration);

    }

    private static class EntryData {
        private final double[] data;
        private final String image;
        private final double intensity;


        public EntryData(double[] data, double intensity, String image){
            this.data = data;
            this.intensity = intensity;
            this.image = image;
        }
        public double[] getData() {
            return data;
        }
        public double getIntensity() {
            return intensity;
        }
        public int size() {
            return data.length;
        }
    }
}
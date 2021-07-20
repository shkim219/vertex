package kmeans;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.Buffer;

public class test {
    public static void main(String[] args) throws IOException {
        String s = null;
        Process p = Runtime.getRuntime().exec("python C:\\Users\\paulk\\PycharmProjects\\vertex-main\\vertex-main\\shkim219\\query2\\__init__.py");

        BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));

        while ((s = stdInput.readLine()) != null){
            System.out.println(s);
        }
    }
}

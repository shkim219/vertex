package graphql;

import org.apache.commons.exec.CommandLine;
import org.apache.http.HttpResponse;
import org.apache.http.client.fluent.Request;
import org.apache.http.entity.ContentType;
import org.apache.http.util.EntityUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Array;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;

public class Fetch {

    public static void main(String[] args) throws IOException, InterruptedException{
        ArrayList<String> returned = fetch("features.csv");
        for (int i = 0; i < returned.size(); i++){
            System.out.println(returned.get(i));
        }
    }

    public static ArrayList<String> fetch(String filename) throws IOException, InterruptedException {
        /*URL url = new URL("https://api.hypi.app/graphql");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setRequestProperty("Authorization", "eyJhbGciOiJSUzI1NiJ9.eyJoeXBpLmxvZ2luIjp0cnVlLCJoeXBpLnVzZXJuYW1lIjoic2hraW0yMTlAYnUuZWR1IiwiaHlwaS5lbWFpbCI6InNoa2ltMjE5QGJ1LmVkdSIsImF1ZCI6IjAxRjdWNDE3MFpERFNFWUY4OFZaVDVaNEdGIiwiaWF0IjoxNjI2MTAxNzU2LCJleHAiOjE2Mjg2OTM3NTYsInN1YiI6IjAxRjdWNDE3MFo0R0NDWllSNVcyTTBKUTA0IiwibmJmIjoxNjI2MTAxNzU2fQ.FEw4oK6yaVSZUukvdPES7RqvmaFyTJZpUVxqDnhcdLwsLaosni5dJn0FTjNURt_rMuqfgpz4ijWJ18od7q1GhcOjfPodtUJjM_uv0j3LUcA0DYX9_MKw0LGjlhfK93t2h8zCMXQUfkjjB2ZYPObHkBteshlswtJDhP39q1jQzLHu0ElnYTrM1ZrQ33SfbTbX6QsVzhIEky-rkgkcoVan9_RDfNNrI6GqMsGFp1clWS7dZSROEMIWpe_1mEXWo2xBepJ0ixzEjeOyunnRhihzRQFV-3JrXgK9Skg1O944DOqvyKDDJ-fd7V7qNPTKLV6mNUwO2L3c4KR7YdE_9ERwtA");
        connection.setRequestProperty("hypi-domain", "clamming.apps.hypi.app");

        System.out.println(connection.getResponseCode() + " " + connection.getResponseMessage());
        connection.disconnect();*/


        /*Request request = Request.Post("https://api.hypi.app/graphql");
        String body = "{\n" +
                "            find(type: Filename, arcql: \"* SORT hypi.id ASC\"){\n" +
                "                edges {\n" +
                "                    node {\n" +
                "                        ... on Filename {\n" +
                "                            csvname\n" +
                "                            totalnumber\n" +
                "                        }\n" +
                "                    }\n" +
                "                }\n" +
                "            }\n" +
                "        }";
        //System.out.println(body);
        request.bodyString(body, ContentType.APPLICATION_JSON);
        request.setHeader("Content-Type", "application/json");
        request.setHeader("Authorization", "eyJhbGciOiJSUzI1NiJ9.eyJoeXBpLmxvZ2luIjp0cnVlLCJoeXBpLnVzZXJuYW1lIjoic2hraW0yMTlAYnUuZWR1IiwiaHlwaS5lbWFpbCI6InNoa2ltMjE5QGJ1LmVkdSIsImF1ZCI6IjAxRjdWNDE3MFpERFNFWUY4OFZaVDVaNEdGIiwiaWF0IjoxNjI2MTAxNzU2LCJleHAiOjE2Mjg2OTM3NTYsInN1YiI6IjAxRjdWNDE3MFo0R0NDWllSNVcyTTBKUTA0IiwibmJmIjoxNjI2MTAxNzU2fQ.FEw4oK6yaVSZUukvdPES7RqvmaFyTJZpUVxqDnhcdLwsLaosni5dJn0FTjNURt_rMuqfgpz4ijWJ18od7q1GhcOjfPodtUJjM_uv0j3LUcA0DYX9_MKw0LGjlhfK93t2h8zCMXQUfkjjB2ZYPObHkBteshlswtJDhP39q1jQzLHu0ElnYTrM1ZrQ33SfbTbX6QsVzhIEky-rkgkcoVan9_RDfNNrI6GqMsGFp1clWS7dZSROEMIWpe_1mEXWo2xBepJ0ixzEjeOyunnRhihzRQFV-3JrXgK9Skg1O944DOqvyKDDJ-fd7V7qNPTKLV6mNUwO2L3c4KR7YdE_9ERwtA");
        request.setHeader("Hypi-Domain", "clamming.apps.hypi.app");
        HttpResponse httpResponse = request.execute().returnResponse();
        System.out.println(httpResponse.getStatusLine());
        if (httpResponse.getEntity() != null) {
            String html = EntityUtils.toString(httpResponse.getEntity());
            System.out.println(html);
        }*/

        String path = "C:\\Users\\paulk\\PycharmProjects\\vertex-main\\vertex-main\\shkim219\\query\\__init__.py";
        ProcessBuilder pb = new ProcessBuilder("python", path, filename);//.inheritIO();
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
        System.out.println(count);
        p.waitFor();
        return fetched;

    }
}

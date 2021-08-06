package randomforest;

import com.opencsv.CSVWriter;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class CSVCreator {
    public static void main(String[] args) throws IOException{
        File readFile = new File("C:\\Users\\paulk\\IdeaProjects\\skopytest\\test.txt");
        File file = new File("data.csv");
        try {
            Scanner sc = new Scanner(readFile);
            FileWriter out = new FileWriter(file);
            CSVWriter writer = new CSVWriter(out);
            while(sc.hasNextLine()){
                String line = sc.nextLine();
                String error = line.substring(0,line.indexOf(" for"));
                String numTrees = line.substring(line.indexOf("for") + 4, line.indexOf(" number"));
                String[] toAdd = new String[]{numTrees, error};
                writer.writeNext(toAdd);
            }
            writer.close();
        }
        catch (IOException e){
            e.printStackTrace();
        }
    }
}

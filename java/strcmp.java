import java.io.*;
import java.util.Map;
import java.util.List;
import java.util.Random;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;


public class strcmp {

    public static void main(String[] args) {
        List<Tuple> tests = new ArrayList<>();

        try{
            FileInputStream fstream = new FileInputStream("../tests.csv");
            BufferedReader br = new BufferedReader(new InputStreamReader(fstream));

            String strLine;

            while ((strLine = br.readLine()) != null)   {
                String[] parts = strLine.split(",");
                String str_a = parts[0];
                String str_b = parts[1];

                Tuple tuple = new Tuple(str_a, str_b);
                tests.add(tuple);
            }

            br.close();
        }catch (Exception e){
            System.err.println("Error: " + e.getMessage());
        }

        measureTimes(tests);
    }


    static boolean naiveStrCompare(String a, String b){
        if (a.length() != b.length()){
            return false;
        }

        char chA[] = a.toCharArray();
        char chB[] = b.toCharArray();

        for(int i=0; i<a.length(); i++){
            if (chA[i] != chB[i]){
                return false;
            }

            try {
                // 1 ms
                Thread.sleep(1);
            } catch(InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
        }

        return true;
    }

    static void measureTimes(List<Tuple> tests)
    {
        int samples = 500000;

        boolean temp = false;

        long startTime;
        long endTime;
        long duration = 0;

        String a = "";
        Random seed = new Random(42);

        Map<String, Long> measurements = new LinkedHashMap<String, Long>();

        // Initialize result map
        for (Tuple test : tests) {
            measurements.put(test.b, duration);
        }

        for(int i = 0; i < samples; i++)
        {
            // Randomize test order
            Collections.shuffle(tests, seed);

            // Run all tests
            for (Tuple test : tests) {
                a = test.a;
                String b = test.b;

                startTime = System.nanoTime();

                //temp = naiveStrCompare(a, b);
                temp = a.equals(b);

                endTime = System.nanoTime();

                // accounting
                long currentDuration = measurements.get(b);
                measurements.put(b, currentDuration + endTime - startTime);
            }
        }

        for (String bIter : measurements.keySet()) {
            System.out.println(a + "," + bIter + "," + samples + "," + measurements.get(bIter));
        }
    }
}

class Tuple {
    public final String a;
    public final String b;
    public Tuple(String a, String b) {
      super();
      this.a = a;
      this.b = b;
    }
}

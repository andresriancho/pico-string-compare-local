import java.io.*;

public class strcmp {

    public static void main(String[] args) {
        try{
            FileInputStream fstream = new FileInputStream("../tests.csv");
            BufferedReader br = new BufferedReader(new InputStreamReader(fstream));

            String strLine;

            while ((strLine = br.readLine()) != null)   {
                String[] parts = strLine.split(",");
                String str_a = parts[0];
                String str_b = parts[1];
                TimeCompare(str_a, str_b);
            }

            br.close();
        }catch (Exception e){
            System.err.println("Error: " + e.getMessage());
        }
    }


    static void TimeCompare(String a, String b)
    {
        int samples = 500000;
        boolean temp = false;
        long startTime;
        long endTime;
        long duration = 0;

        for(int i = 0; i < samples; i++)
        {
            startTime = System.nanoTime();

            temp = a.equals(b);

            endTime = System.nanoTime();
            duration += endTime - startTime;
        }

        System.out.println(a + "," + b + "," + samples + "," + duration);

    }
}
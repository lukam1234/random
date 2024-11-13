using System.Diagnostics;
using System;
using System.Text;

class ADBwrapper
{
    private static StreamWriter logWriter;
    //main function to obtain user input and call functions
    private static void Main()
    {
        //logWriter path hardcoded for now.
        logWriter = new StreamWriter("C:\\Users\\luka.moon\\Documents\\a.txt", append: true);
        Console.SetOut(new StreamWriter(Console.OpenStandardOutput()) { AutoFlush = true });
        Console.SetIn(new StreamReader(Console.OpenStandardInput()));
        string phonePath, localPath;
        Console.WriteLine("enter path of file on phone");
        LogOutput("enter path of file on phone");
        phonePath = Console.ReadLine();
        Console.WriteLine("enter path of local file to extract to");
        LogOutput("enter path of local file to extract to");
        localPath = Console.ReadLine();
        LogInput(phonePath);
        LogInput(localPath);
        
        try
        {
            adbDaemon();
            adbPull(phonePath, localPath);
            logWriter.Close();
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine("File not found");
        }
    }
//ensure adb server is running/log output
    static void adbDaemon()
    {
        Process adbDaemon = new Process();
        adbDaemon.StartInfo.FileName = "adb.exe";
        adbDaemon.StartInfo.Arguments = "start-server";
        adbDaemon.StartInfo.RedirectStandardOutput = true;
        adbDaemon.StartInfo.RedirectStandardError = true;
        adbDaemon.StartInfo.UseShellExecute = false;
        
        adbDaemon.OutputDataReceived += (sender, e) =>
        {
            if (e.Data != null)
            {
                Console.WriteLine(e.Data);
                logWriter.WriteLine($"Output: {e.Data}");
            }
        };
        
        adbDaemon.ErrorDataReceived += (sender, e) =>
        {
            if (e.Data != null)
            {
                Console.WriteLine(e.Data);
                logWriter.WriteLine($"Output: {e.Data}");
            }
        };
        adbDaemon.Start();
        adbDaemon.BeginOutputReadLine();
        adbDaemon.BeginErrorReadLine();
        adbDaemon.WaitForExit();
        
    }
//method for pulling file from device, also logs output
    static void adbPull(string phone, string local)
    {
        Process adb = new Process();
        adb.StartInfo.FileName = "adb.exe";
        adb.StartInfo.RedirectStandardOutput = true;
        adb.StartInfo.RedirectStandardError = true;
        adb.StartInfo.UseShellExecute = false; 
        adb.StartInfo.CreateNoWindow = true;     
        adb.StartInfo.Arguments = "pull" + " " + phone + " " + local;
        //log output data
        adb.OutputDataReceived += (sender, e) =>
        {
            if (e.Data != null)
            {
                Console.WriteLine(e.Data);
                logWriter.WriteLine($"Output: {e.Data}");
            }
        };
        //log err data
        adb.ErrorDataReceived += (sender, e) =>
        {
            if (e.Data != null)
            {
                Console.WriteLine(e.Data);
                logWriter.WriteLine($"Output: {e.Data}");
            }
        };
        adb.Start();
        adb.BeginOutputReadLine();
        adb.BeginErrorReadLine();
        adb.WaitForExit();
        //issues stem mainly from the program exiting before allowing adb to finish executing, resulting in no logs.
        //fixed with waitforexit
    }
    //loggers
    static void LogInput(string input)
    {
        logWriter.WriteLine($"userInput: {input}");
    }
    static void LogOutput(string output)
    {
        logWriter.WriteLine($"Output: {output}");
    }
}

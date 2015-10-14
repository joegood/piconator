using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Piconator.Classes
{

    public enum PlatformInfo
    {
        Unknown = 0,
        Windows = 1,
        Linux = 2
    }

    /// <summary>
    /// Decides the run-time parameters for the app, by ways of OS enviornment variables, OS itself, files, and command line options.
    /// </summary>
    class RunParams
    {

        public RunParams()
        {

            Console.WriteLine("OSVersion = {0}", System.Environment.OSVersion);

            // Determine the OS
            // Research this..
            this.Platform = PlatformInfo.Windows;
    
        }

        public PlatformInfo Platform { get; set; }

    }
}

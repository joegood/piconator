using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Piconator.Classes;

namespace Piconator
{
    class Program
    {
        static void Main(string[] args)
        {
            // Set up the size of the console window.  Curious, what does this do under Linux?

            // I'm abandoning the idea of animating the GIF in the console but will still use the console for analysis, if command line
            // options are present to direct that.

            double ratio = 0.9;
            Console.SetWindowSize((int)Math.Round(Console.LargestWindowWidth * ratio), (int)Math.Round(Console.LargestWindowHeight * ratio));
            Console.SetBufferSize(Console.WindowWidth, 10000);

            Console.CursorSize = 5;

            Console.WriteLine("CursorLeft = {0}   CursorSize = {1}  CursorTop={2}  CursorVisible={3}", Console.CursorLeft, Console.CursorSize, Console.CursorTop, Console.CursorVisible);

            var gInfo = ImageLib.Analyze("anim/matrix.gif");
            foreach( string line in gInfo)
            {
                Console.WriteLine(line);
            }
            Console.WriteLine("");

            gInfo = ImageLib.Analyze("stills/pacman-blinky.png");
            foreach ( string line in gInfo)
            {
                Console.WriteLine(line);
            }
            Console.WriteLine("");

            var conSize = new System.Drawing.Rectangle(Console.WindowLeft, Console.WindowTop, Console.WindowWidth, Console.WindowHeight);
            Console.WriteLine("Console Size = {0}", conSize.ToString());



            Console.WriteLine("Press any key to start anim...");
            Console.ReadKey();

            var imgLib = new ImageLib();
            imgLib.LoadImage("anim/matrix.gif");

        }
    }
}

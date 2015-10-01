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

            double ratio = 0.9;
            Console.SetWindowSize((int)Math.Round(Console.LargestWindowWidth * ratio), (int)Math.Round(Console.LargestWindowHeight * ratio));
            Console.SetBufferSize(Console.WindowWidth, 10000);

            Console.CursorSize = 5;

            Console.WriteLine("CursorLeft = {0}   CursorSize = {1}  CursorTop={2}  CursorVisible={3}", Console.CursorLeft, Console.CursorSize, Console.CursorTop, Console.CursorVisible);

            var gInfo = ImageLib.AnalyzeV1("anim/matrix.gif");
            foreach( string line in gInfo)
            {
                Console.WriteLine(line);
            }
            Console.WriteLine("");

            gInfo = ImageLib.AnalyzeV1("stills/pacman-blinky.png");
            foreach ( string line in gInfo)
            {
                Console.WriteLine(line);
            }
            Console.WriteLine("");



            Console.WriteLine("Press any key to start anim...");
            Console.ReadKey();

            int counter;
            string[] sequence;

            counter = 0;
            sequence = new string[] { "/", "-", "\\", "|" };
            sequence = new string[] { ".", "o", "0", "o" };
            sequence = new string[] { "+", "x" };
            sequence = new string[] { "V", "<", "^", ">" };
            //sequence = new string[] { ".   ", "..  ", "... ", "...." };

            for (int n = 0; n <= 10000; n++)
            {
                counter++;

                if (counter >= sequence.Length)
                    counter = 0;

                Console.Write(sequence[counter]);
                Console.SetCursorPosition(Console.CursorLeft - sequence[counter].Length, Console.CursorTop);
            }

            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();

        }
    }
}

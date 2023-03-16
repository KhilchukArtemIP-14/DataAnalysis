using System;
using Microsoft.EntityFrameworkCore.SqlServer;
using ADIS_lab1.Models;
using Microsoft.VisualBasic.FileIO;
using System.Globalization;

namespace ADIS_lab1
{
    class Program
    {
        static void Main(string[] args)
        {
            ETLService etl = new ETLService(new DotaMatchesContext());

            etl.InitialLoad();
        }
    }
}

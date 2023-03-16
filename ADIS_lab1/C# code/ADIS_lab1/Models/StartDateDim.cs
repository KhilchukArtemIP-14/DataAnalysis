using System;
using System.Collections.Generic;

#nullable disable

namespace ADIS_lab1.Models
{
    public partial class StartDateDim
    {
        public StartDateDim()
        {
            MatchFacts = new HashSet<MatchFact>();
        }

        public int RelativeDateInSeconds { get; set; }
        public DateTime AbsoluteDateTime { get; set; }
        public DateTime Date { get; set; }
        public int DayOfMonth { get; set; }
        public TimeSpan Time { get; set; }
        public int Hours { get; set; }
        public int Minutes { get; set; }

        public virtual ICollection<MatchFact> MatchFacts { get; set; }
    }
}

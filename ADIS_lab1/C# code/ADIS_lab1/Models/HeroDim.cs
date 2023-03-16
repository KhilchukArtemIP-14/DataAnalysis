using System;
using System.Collections.Generic;

#nullable disable

namespace ADIS_lab1.Models
{
    public partial class HeroDim
    {
        public HeroDim()
        {
            InverseRef = new HashSet<HeroDim>();
            PlayerFacts = new HashSet<PlayerFact>();
        }

        public int HeroId { get; set; }
        public string HeroName { get; set; }
        public DateTime EffStartDate { get; set; }
        public DateTime EffEndDate { get; set; }
        public int? RefId { get; set; }

        public virtual HeroDim Ref { get; set; }
        public virtual ICollection<HeroDim> InverseRef { get; set; }
        public virtual ICollection<PlayerFact> PlayerFacts { get; set; }
    }
}

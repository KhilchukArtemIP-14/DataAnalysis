using System;
using System.Collections.Generic;

#nullable disable

namespace ADIS_lab1.Models
{
    public partial class SlotDim
    {
        public SlotDim()
        {
            PlayerFacts = new HashSet<PlayerFact>();
        }

        public int CodeId { get; set; }
        public string Team { get; set; }

        public virtual ICollection<PlayerFact> PlayerFacts { get; set; }
    }
}

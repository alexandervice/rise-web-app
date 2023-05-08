// Trying to get an idea for how I will organize the MongoDB database

// Specializations:
let specializationExample1 = {
  name: "Assassin",
  description: "Focuses on stealth, silence, and one-shot kills.",
  recommendedAttributes: ["Int", "Hrt", "Cha"],
  recommendedStats: ["Spd", "HP"],
  requirements: [
    "Successfully perform 3 sneak attacks",
    "Assassinate and kill a target with a sneak attack on 3 separate occasions.",
    "Assassinate and kill a public or famous figure without being caught."
  ],
  ranks: [
    {
      rankNumber: 1,
      type: "Power",
      description: "When sneak attacking a target while using a light weapon your attack is penetrating and ignores the target's armor."
    },
    {
      rankNumber: 2,
      type: "Stunt",
      name: "Must Have Been the Wind",
      cost: 5,
      description: "If performing this action while sneaking, your stealth is not broken."
    },
    {
      rankNumber: 3,
      type: "Action",
      name: "Analytical Eye",
      actionType: "Minor",
      description: "Examine a humanoid target that you can see within 10 m of you to attempt to determine their weakness. Gain +2 towards targeting tests against this foe for the remainder of the encounter."
    }
    // the rest of the ranks would go here
  ]

}

let specializationExample2 = {
  name: "Cleric",
  description: "The worlds greatest healers, able to mend bones, cure disease, and even prevent death.",
  recommendedAttributes: ["Int", "End", "Hrt"],
  recommendedStats: ["HP", "MP"],
  requirements: [
    "Heal a non party member who is injured, sick, or in pain.",
    "Help others recover a total of 150 recovered HP.",
    "Save 5 total people who were on the brink of death with your healing."
  ],
  ranks: [
    {
      rankNumber: 1,
      type: "spell",
      spells: [
        {
          name: "Metabolize",
          category: "Restoration",
          attribute: "Int",
          level: "Novice",
          specialization: "Cleric",
          cost: 4,
          action: "Major",
          range: "Touch",
          targetsOrArea: "1 Target",
          description: "Negate the effects of a potion, poison, or venom on a target. (test roll determined by the strength of potion/poison). Some more potent poisons require extended time to cure. Recovering from drunkeness requires a TN that changes based on how drunk the character is, with Buzzed requiring a TN of 12 and for every level after the TN increases by 2.  Characters that receive any form of magical healing cannot benefit from magical healing again until they take additional damage. (this spell can be used to cure hangovers)",
          targetNumber: "varies",
          concentration: "yes"
        },
        {
          name: "Healing Aura",
          category: "Restoration",
          attribute: "Int",
          level: "Novice",
          specialization: "Cleric",
          cost: 6,
          action: "Major",
          range: "5 m",
          targetsOrArea: "Self / All Allies",
          description: "Emit an aura of regenerative arcana around yourself that heals yourself and your allies by 1d6 hp for each round you maintain concentration (maximum 3 rounds).",
          targetNumber: 14,
          concentration: "yes"
        }
      ]
    },
    {
      rankNumber: 2,
      type: "Stunt",
      name: "Healer's Spirit",
      cost: 3,
      description: "Recover half of the HP you just restored to another. (this stunt can only be used immediately after healing a target with a restoration spell)"
    },
    {
      rankNumber: 3,
      type: "Power",
      description: "All of your healing Restoration Arcana  now add your Heart attribute modifier to HP recovered."
    }
    // the rest of the ranks would go here
  ]

}
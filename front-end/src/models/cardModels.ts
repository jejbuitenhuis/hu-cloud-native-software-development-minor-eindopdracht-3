export type PrintCard = {
  PK: string,
  SK: string,
  OracleId: string,
  OracleName: string,
  PrintId: string,
  Price: number | null,
  ReleasedAt: string,
  SetName: string,
  Rarity: "common" | "uncommon" | "rare" | "mythic",
  CardFaces: PrintFace[],
}
export type PrintFace = {
  Colors: string[],
  FaceName: string,
  FlavorText: string,
  ImageUrl: string,
  ManaCost: string,
  OracleText: string,
  TypeLine: string,
}
export type DeckCard = {
  PK: string,
  SK: string,
  card_location: string,
  CardFaces: CardFaceWrapper[]
  data_type: string,
  deck_card_id: string,
  deck_id: string,
  OracleId: string,
  OracleName: string,
  Price: number,
  PrintId: string,
  Rarity: string,
  ReleasedAt: string,
  SetName: string,
  user_id: string
}

export type CardFaceWrapper = {
  M: CardFace
}

export type CardFace = {
  Colors: {
    L: Color[]
  },
  FlavorText: {
    "S": string
  },
  ManaCost: {
    "S": string
  },
  TypeLine: {
    "S": string
  },
  ImageUrl?: {
    "S": string
  },
  FaceName: {
    "S": string
  },
  OracleText: {
    "S": string
  }
}

export type Color = {
  "S": string
}
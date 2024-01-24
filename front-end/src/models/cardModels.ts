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
export interface CardData {
  cardInstanceId?: string,
  cardLocation: string,
  card: PrintCard,
}
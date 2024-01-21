export type PrintCard = {
  PK: string,
  SK: string,
  GSI1PK: string,
  GSI1SK: string,
  DataType: "Card",
  OracleName: string,
  Price: number | null,
  Rarity: "common" | "uncommon" | "rare" | "mythic",
  ReleasedAt: string,
  SetName: string,
}
export type PrintFace = {
  PK: string,
  SK: string,
  GSI1PK: string,
  GSI1SK: string,
  DataType: "Face",
  Colors: string,
  FaceName: string,
  FlavorText: string,
  ImageUrl: string,
  ManaCost: string,
  OracleText: string,
  TypeLine: string,
}
export type PrintPart = PrintCard | PrintFace;
export type CombinedPrint = PrintCard & {
  Faces: PrintFace[]
}
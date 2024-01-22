export type PrintCard = {
  PK: string,
  SK: string,
  OracleId: string,
  PrintId: string,
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
  OracleId: string,
  PrintId: string,
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
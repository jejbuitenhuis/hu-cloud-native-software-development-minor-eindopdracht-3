interface CardsSearchResponse {
    object : string,
    total_cards: string,
    has_more: boolean,
    next_page: string,
    data : object[],
}
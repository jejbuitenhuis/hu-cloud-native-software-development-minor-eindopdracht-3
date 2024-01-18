describe("HomeView", () => {
	it("navigates to create deck when create new deck button is pressed", () => {
		cy.visit("/");

		cy.getByTestId("create-deck")
			.clickAtTop();

		cy.location("hash")
			.should("equal", "#/decks/new/");
	});
});

describe("My First Test", () => {
	it("visits the app root url and types into the input field", () => {
		cy.visit("/");

		cy.contains("h1", "Hello, World!");

		const toType = "My First Test";

		cy.getByTestId("input")
			.shadow()
			.find("input")
			.type(toType);

		cy.getByTestId("something")
			.should("contain.text", toType);
	});
});
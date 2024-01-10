/// <reference types="cypress" />

Cypress.Commands.add("getByTestId", (selector, ...args) => {
	return cy.get(`[data-test-id=${selector}]`, ...args);
});

export {};

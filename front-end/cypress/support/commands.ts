/// <reference types="cypress" />

Cypress.Commands.add("getByTestId", (selector, ...args) => {
	return cy.get(`[data-test-id=${selector}]`, ...args);
})
// @ts-ignore
Cypress.Commands.add('clickAtTop', { prevSubject: 'element' }, (subject) => {
	// @ts-ignore
	cy.wrap(subject).click({ position: 'top' });
});
export {};

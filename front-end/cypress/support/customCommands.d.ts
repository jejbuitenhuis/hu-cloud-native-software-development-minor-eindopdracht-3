// customCommands.d.ts

declare namespace Cypress {
    interface Chainable<Subject = any> {
      /**
       * Custom command to select elements by data-testid attribute
       * @example cy.getByTestId('some-test-id')
       */
      getByTestId(value: string): Chainable<JQuery<HTMLElement>>;
    }
  }
  
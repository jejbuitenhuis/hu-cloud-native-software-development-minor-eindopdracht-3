describe("Register page Test", () => {
   
    beforeEach(()=>{
        cy.visit("/register");
    })
    
    it("Registers the user in correctly", () => {
        cy.getByTestId('email').shadow().find("input").type('test@example.com')
        cy.getByTestId('password').shadow().find("input").type('testtest')
        cy.getByTestId('confirm').shadow().find("input").type('testtest')
        cy.getByTestId('submit').shadow().find('button').clickAtTop()
        cy.contains("We have send you an email to verify your email adress.")
    })

    it("Registers when user already exists", () => {
        cy.getByTestId('#email').shadow().find("input").type('test@example.com')
        cy.getByTestId('#password').shadow().find("input").type('testtest')
        cy.getByTestId('#confirm').shadow().find("input").type('testtest')
        cy.getByTestId('#submit').shadow().find('button').clickAtTop()
        
        
        cy.getByTestId('#email').shadow().type('test@example.com')
        cy.getByTestId('#password').shadow().type('testtest')
        cy.getByTestId('#confirm').shadow().find('input').type('testtest')
        cy.getByTestId('#submit').shadow().find('button').clickAtTop()

        cy.contains("This email adress has already been registered!")
    })

});
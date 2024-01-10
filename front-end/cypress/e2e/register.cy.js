describe("Register page Test", () => {
   
    beforeEach(()=>{
        cy.visit("/register");
    })
    
    it("Registers the user in correctly", () => {
        cy.get('#email').find("input").type('test@example.com')
        cy.get('#password').find("input").type('testtest')
        cy.get('#confirm').find("input").type('testtest')
        cy.get('#submit').find('button').click({ position: 'top' })
        cy.contains("We have send you an email to verify your email adress.")
    })

    it("Registers when user already exists", () => {
        cy.get('#email').find("input").type('test@example.com')
        cy.get('#password').find("input").type('testtest')
        cy.get('#confirm').find("input").type('testtest')
        cy.get('#submit').find('button').click({ position: 'top' })
        
        
        cy.get('#email').type('test@example.com')
        cy.get('#password').type('testtest')
        cy.get('#confirm').find('input').type('testtest')
        cy.get('#submit').find('button').click({ position: 'top' })

        cy.contains("This email adress has already been registered!")
    })
});
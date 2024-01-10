describe("Register page Test", () => {
    beforeEach(()=>{
        cy.visit("/register");
    })
    
    it("Registers the user in correctly", () => {
        cy.get('#email').shadow().find("input").type('test@example.com')
        cy.get('#password').shadow().find("input").type('testtest')
        cy.get('#confirm').shadow().find("input").type('testtest')
        cy.get('#submit').shadow().find("button").click()
        cy.contains("We have send you an email to verify your email adress.")
    })

    it("Registers in with incorrect password", () => {
        cy.get('#email').shadow().find("input").type('test@example.com')
        cy.get('#password').shadow().find("input").type('testtest')
        cy.get('#confirm').shadow().find("input").type('testtest')
        cy.get('#submit').shadow().find("button").click()
        cy.contains("Passwords must match!")
    })

    it("Registers in with incorrect email", () => {
        cy.get('#email').shadow().find("input").type('test@example.com')
        cy.get('#password').shadow().find("input").type('testtest')
        cy.get('#confirm').shadow().find("input").type('testtest')
        cy.get('#submit').shadow().find("button").click()
        cy.contains("This is not a correct email!")
    })
   
    it("Registers when user already exists", () => {
        cy.get('#email').type('test@example.com')
        cy.get('#password').type('testtest')
        cy.get('#confirm').type('testtest')
        cy.get('#submit').click()
        
        cy.get('#email').type('test@example.com')
        cy.get('#password').type('testtest')
        cy.get('#confirm').type('testtest')
        cy.get('#submit').click()

        cy.contains("This email adress has already been registered!")
    })
});
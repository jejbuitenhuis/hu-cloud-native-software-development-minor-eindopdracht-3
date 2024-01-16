// @ts-ignore
import { v4 as uuidv4} from 'uuid';

describe("Register page Test", () => {
	const firstEmail = `test-${uuidv4()}@example.com`;
	const secondEmail = `test-${uuidv4()}@example.com`;

	beforeEach(()=>{
		cy.visit("/register");
	});

	it("Registers the user in correctly", () => {
		cy.getByTestId('email')
			.shadow()
			.find("input")
			.type(firstEmail);
		cy.getByTestId('password')
			.shadow()
			.find("input")
			.type('testtest');
		cy.getByTestId('confirm')
			.shadow()
			.find("input")
			.type('testtest');
		cy.getByTestId('submit')
			.shadow()
			.find('button')
			.clickAtTop();
		cy.on('window:alert', (str) => {
			expect(str).to.equal(`We have send you an email to verify your email adress.`)
		  })
	});

	it("Registers when user already exists", () => {
		cy.getByTestId('email')
		.shadow()
		.find("input")
		.type(secondEmail)
			
		cy.getByTestId('password')
		.shadow()
		.find("input")
		.type('testtest')

		cy.getByTestId('confirm')
		.shadow()
		.find("input")
		.type('testtest')

		cy.getByTestId('submit')
			.shadow()
			.find('button')
			.clickAtTop();

		cy.visit("/register");

		cy.getByTestId('email')
		.shadow()
		.find("input")
		.type(secondEmail)

		cy.getByTestId('password')
		.shadow()
		.find("input")
		.type('testtest')

		cy.getByTestId('confirm')
		.shadow()
		.find("input")
		.type('testtest')

		cy.getByTestId('submit')
			.shadow()
			.find('button')
			.clickAtTop();

		cy.contains("This email adress has already been registered!");
	});
});

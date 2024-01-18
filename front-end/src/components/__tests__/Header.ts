import { mount } from "@vue/test-utils";
import Hello from "../Header.vue";

describe("Title component", () => {
	let element: ReturnType<typeof mount>;

	beforeEach(() => {
		element = mount(Hello, {});
	});

	it("should create a component", () => {
		expect(element).toBeTruthy();
	});

	it("should contain the title of the application", () => {
		expect( element.text() ).toEqual("Dragons MTG Card Collection System");
	});
});

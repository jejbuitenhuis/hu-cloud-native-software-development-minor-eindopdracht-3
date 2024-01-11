import { mount } from "@vue/test-utils";
import Hello from "../Title.vue";

describe("Title component", () => {
	let element: ReturnType<typeof mount>;

	beforeEach(() => {
		element = mount(Hello, {});
	});

	it("should create a component", () => {
		expect(element).toBeTruthy();
	});

	it("should contain the text 'Hello, World!'", () => {
		expect( element.text() ).toEqual("Hello, World!");
	});
});

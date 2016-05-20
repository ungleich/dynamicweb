$( document ).ready(function() {

	//we need to load first VMTypesData from base.html django template
	var pricingData = window.VMTypesData;


	// Function to calculate the price given a vm type
	function calculate_price(vm_type){

		var ID_SELECTOR = "#";
		var CURRENCY = "CHF";
		var final_price_selector = ID_SELECTOR.concat(vm_type.concat('-final-price'));
		var final_price_input_selector = final_price_selector.concat('-input');
		var core_selector = ID_SELECTOR.concat(vm_type.concat('-cores'));
		var memory_selector = ID_SELECTOR.concat(vm_type.concat('-memory'));
		var disk_size_selector = ID_SELECTOR.concat(vm_type.concat('-disk_space'));

		//Get vm type prices
		var cores = $(core_selector).val();
		var memory = $(memory_selector).val();
		var disk_size = $(disk_size_selector).val();
		var pricingData = eval(window.VMTypesData);
		var company_prices = _.head(_.filter(pricingData, {hosting_company: vm_type}));

		//Calculate final price
		var price = company_prices.base_price;
			price += company_prices.core_price*cores;
			price += company_prices.memory_price*memory;
			price += company_prices.disk_size_price*disk_size;
		
		console.log(final_price_input_selector);
		$(final_price_selector).text(price.toString().concat(CURRENCY));
		$(final_price_input_selector).attr('value', price);

	}

	//Listener function
	function change_attribute(e){

		var vm_type = this.getAttribute('data-vm-type');
		calculate_price(vm_type);
	}


	//Listeners
	$('.cores-selector').on('change',change_attribute);

	$('.memory-selector').on('change',change_attribute);

	$('.disk-space-selector').on('change',change_attribute);

	//Disable input
	$('.disk-space-selector').keypress(function(event){
    	event.preventDefault();
	});

});
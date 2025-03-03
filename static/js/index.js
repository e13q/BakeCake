function showModal(message) {
    document.getElementById('modal-message').innerHTML = message; // Вставляем HTML в модальное окно
    document.getElementById('myModal').style.display = "block"; // Показываем модальное окно
}

document.querySelector(".extra_close").onclick = function() {
    document.getElementById('myModal').style.display = "none";
}

Vue.createApp({
    name: "App",
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            schema1: {
                lvls: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' количество уровней';
                },
                form: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' форму торта';
                },
                topping: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' топпинг';
                }
            },
            schema2: {
                name: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' имя';
                },
                phone: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' телефон';
                },
                name_format: (value) => {
                    const regex = /^[a-zA-Zа-яА-Я]+$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат имени нарушен';
                    }
                    return true;
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                phone_format:(value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email: (value) => {
                    if (value) {
                        return true;
                    }
                    return '⚠ Необходимо указать почту';
                },
                address: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' адрес';
                },
                date: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' дату доставки';
                },
                time: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' время доставки';
                }
            },
            DATA: DATA,
            Costs: COSTS,
            Levels: 0,
            Form: 0,
            Topping: 0,
            Berries: 0,
            Decor: 0,
            Words: '',
            Comments: '',
            Designed: false,
            Name: USER.Name,
            Email: USER.Email,
            Phone: USER.Phone,            
            Address: null,
            Dates: null,
            Time: null,
            DelivComments: '',
            errors: {
                order_date: []
            },
            errorsKey: 0
        }
    },
    methods: {
        ToStep4() { 
            this.Designed = true
            setTimeout(() => this.$refs.ToStep4.click(), 0);
        },
        submitForm() {               
            $("#loadingOverlay").show();
            $.ajax({
                url: '/create-order/',
                method: 'POST',
                data: {
                    csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
                    level: this.DATA.Levels[this.Levels],
                    form: this.DATA.Forms[this.Form],
                    topping: this.DATA.Toppings[this.Topping],
                    berry: this.Berries == 0 ? "" : this.DATA.Berries[this.Berries],
                    decor: this.Decor == 0 ? "" : this.DATA.Decors[this.Decor],
                    words: this.Words,
                    order_comment: this.Comments,
                    full_name: this.Name,
                    email: this.Email,
                    phone_number: this.Phone,
                    address: this.Address,
                    order_date: this.Dates,
                    order_time: this.Time,
                    delivery_comment: this.DelivComments
                },
                success: (response) => {                
                    $("#loadingOverlay").hide();
                    if (response.success) {
                        showModal(response.message);
                        this.errors = {};
                        }
                    else {
                        this.$refs.form.setErrors(response.errors);

                    }
                },
                error: function (xhr, status, error) {                
                    $("#loadingOverlay").hide();
                    alert("Произошла ошибка: " + error);
                }
              });
        }
    },
    computed: {
        Cost() {
            let W = this.Words ? this.Costs.Words : 0
            let price = (this.Costs.Levels[this.Levels] + this.Costs.Forms[this.Form] +
                this.Costs.Toppings[this.Topping] + this.Costs.Berries[this.Berries] +
                this.Costs.Decors[this.Decor] + W) 
            if (!this.Dates || !this.Time) return price;
            let selectedDateTime = new Date(`${this.Dates}T${this.Time}`);
            let now = new Date();
            let timeDiff = selectedDateTime - now;
            let hoursDiff = timeDiff / (1000 * 60 * 60);
            price = hoursDiff < 24 ? `(+20% за <24 часов) ${price * 1.2}` : price
            return price;
        }
    }
}).mount('#VueApp')
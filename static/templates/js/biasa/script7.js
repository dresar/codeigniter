var messageInput = document.createElement("input");
messageInput.setAttribute("type", "text");
messageInput.setAttribute("name", "robot_field");
messageInput.setAttribute("placeholder", "Enter your message");
messageInput.setAttribute("class", "d-none")

// Create the form start time input
var formStartTimeInput = document.createElement('input');
formStartTimeInput.setAttribute('type', 'text');
formStartTimeInput.setAttribute('name', 'form_start_time');
formStartTimeInput.setAttribute('value', Math.floor(Date.now() / 1000)); // Current time in seconds
formStartTimeInput.setAttribute("class", "d-none")

// Create the bot check input
var botCheckInput = document.createElement('input');
botCheckInput.setAttribute('type', 'hidden');
botCheckInput.setAttribute('name', 'bot_check');
botCheckInput.setAttribute('id', 'bot_check');
botCheckInput.setAttribute('value', 232321 + 3202322); // Example bot check value (you can adjust this logic)
botCheckInput.setAttribute("class", "d-none")

var guestbookForm = document.querySelector('.guestbook_form_wrapper form');
if (guestbookForm) {
    guestbookForm.insertBefore(messageInput, guestbookForm.lastElementChild.previousElementSibling);
    guestbookForm.insertBefore(formStartTimeInput, guestbookForm.lastElementChild.previousElementSibling);
    guestbookForm.insertBefore(botCheckInput, guestbookForm.lastElementChild.previousElementSibling);
}

//guest type
var guestTypeInput = document.createElement("input");
guestTypeInput.setAttribute("type", "text");
guestTypeInput.setAttribute("name", "guest_type");
guestTypeInput.setAttribute("class", "d-none")
guestTypeInput.setAttribute("value", guest_type);

var guestbookForm = document.querySelector('.guestbook_form_wrapper form');
if (guestbookForm)
    guestbookForm.insertBefore(guestTypeInput, guestbookForm.lastElementChild.previousElementSibling);

//rsvp
var guestTypeRsvpInput = document.createElement("input");
guestTypeRsvpInput.setAttribute("type", "text");
guestTypeRsvpInput.setAttribute("name", "guest_type");
guestTypeRsvpInput.setAttribute("class", "d-none")
guestTypeRsvpInput.setAttribute("value", guest_type);

var rsvpForm = document.querySelector('#cardRSVP form');
if (rsvpForm)
    rsvpForm.insertBefore(guestTypeRsvpInput, rsvpForm.lastElementChild?.previousElementSibling);

//gift angpo
var guestTypeAngpaoInput = document.createElement("input");
guestTypeAngpaoInput.setAttribute("type", "text");
guestTypeAngpaoInput.setAttribute("name", "guest_type");
guestTypeAngpaoInput.setAttribute("class", "d-none")
guestTypeAngpaoInput.setAttribute("value", guest_type);

var angpaoForm = document.querySelector('.angpao form');
if (angpaoForm)
    angpaoForm.insertBefore(guestTypeAngpaoInput, angpaoForm.lastElementChild.previousElementSibling);

// function addMaxLengthInput() {
var countCharInput = document.createElement("input");
countCharInput.setAttribute("type", "number");
countCharInput.setAttribute("id", "comment_length");
countCharInput.setAttribute("name", "comment_length");
countCharInput.setAttribute("class", "d-none")
countCharInput.setAttribute("value", 0);
countCharInput.setAttribute("data-stepper_id", "{{$stepper->stepper_domain->id}}");
var guestbookForm = document.querySelector('.guestbook_form_wrapper form');
if (guestbookForm)
    guestbookForm.insertBefore(countCharInput, guestbookForm.lastElementChild.previousElementSibling);
// }

// addMaxLengthInput();

function setMaxCharacters(textareaName, maxCharacters) {
    var charCountContainer = document.createElement("div");
    charCountContainer.id = "charCountContainer";
    // charCountContainer.style.marginTop = 0;
    charCountContainer.style.marginBottom = "3px";

    var textarea = document.getElementsByName(textareaName)[0];
    textarea.maxLength = maxCharacters;
    var inputGroupDiv = textarea.closest('.mb-3');
    if (inputGroupDiv) {
        inputGroupDiv.classList.add('textarea-wrapper');
        inputGroupDiv.classList.remove('mb-3')
        inputGroupDiv.insertAdjacentElement('afterend', charCountContainer);
    } else {
        textarea.parentNode.insertBefore(charCountContainer, textarea.nextSibling);
    }
    var bodyColor = getComputedStyle(document.body).color;

    var charCount = document.createElement("div");
    charCount.id = "charCount";
    charCount.textContent = `${(invitation_lang == 'en' ? 'Characters left' : 'Huruf yang Tersisa')}: ${maxCharacters}`;
    charCount.style.textAlign = "left";
    // charCount.style.color = bodyColor;
    // charCount.style.marginTop = 0;
    charCountContainer.appendChild(charCount);

    var currentCharacters = 0;
    textarea.addEventListener("input", function () {
        currentCharacters = this.value.length;
        countCharInput.setAttribute("value", parseInt(currentCharacters));
        charCount.textContent = `${(invitation_lang == 'en' ? 'Characters left' : 'Huruf yang Tersisa')}: ${(maxCharacters - currentCharacters)}`;
    });

    textarea.addEventListener("keyup", function () {
        countCharInput.setAttribute("value", parseInt(textarea.value.length));
    })

    var btnForm = document.getElementById("guestbook_form");
    btnForm.addEventListener("click", function (event) {
        if (countCharInput.value != currentCharacters) {
            alert("Kamu telah melakukan pengeditan Form! ");
            event.preventDefault();
        }
    })
}

if (stepper_id !== 9787) {
    if (guestbookForm)
        setMaxCharacters("comment", 300);
}

// Define mapping
const paymentMap = {
    13736: 50000,
    23301: 50000,
    23760: 99000,
    23761: 179000,
};

// Look up value based on stepper_id
const amount = paymentMap[stepper_id];

if (amount) {
    const paymentInput = document.querySelector('input[name="payment"]');
    if (paymentInput) {
        paymentInput.value = amount;
        paymentInput.disabled = true;
    }

    const form = document.getElementById('formGift');
    if (form) {
        // Ensure hidden input exists or add one
        let hiddenInput = form.querySelector('input[type="hidden"][name="payment"]');
        if (!hiddenInput) {
            hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'payment';
            form.appendChild(hiddenInput);
        }
        hiddenInput.value = amount;

        // Update button text
        const button = form.querySelector('.btn-custom');
        if (button) {
            button.textContent = 'Purchase';
        } else {
            console.warn('No button with class "btn-custom" found inside #formGift.');
        }
    } else {
        console.warn('Form with id "formGift" not found.');
    }
}

const guestName = document.querySelector('h6.greeting-name-text');
const leftContent = document.querySelector('h6.left');
const svg = document.querySelector('h6 span.ml-2');
if (svg) {
    if (guestName) {
        guestName.style.display = 'flex';
        guestName.style.flexWrap = 'wrap';
        guestName.style.alignItems = 'center';
        // guestName.style.lineHeight = '45px';
        svg.style.marginLeft = '0.5rem';
        if (!leftContent)
            guestName.style.justifyContent = 'center';
    }
}
const input_name_angpao = document.getElementById("name_angpao");

if (input_name_angpao && !input_name_angpao.hasAttribute("name")) {
    input_name_angpao.setAttribute("name", "name");
}
const selectStatus = document.querySelector('select[name="status"]');

if (selectStatus && !selectStatus.hasAttribute("required")) {
    selectStatus.setAttribute("required", "");
}

const giftTextMap = {
    13736: "Picnic Story Vol.1", // testing account
    23760: "Picnic Story Vol.1",
    23761: "Picnic Story Vol.1"
};

const textGiftCouple = document.getElementById("text_gift_couple");

if (textGiftCouple && giftTextMap[stepper_id]) {
    textGiftCouple.textContent = giftTextMap[stepper_id];
}

const amountGiftTextMap = {
    13736: "Amount of Purchase", // testing account
    23760: "Amount of Purchase",
    23761: "Amount of Purchase"
};

const amountGiftText = document.getElementById("text_gift_total");

if (amountGiftTextMap && amountGiftTextMap[stepper_id]) {
    amountGiftText.textContent = amountGiftTextMap[stepper_id];
}

const totalGiftTextMap = {
    13736: "Total", // testing account
    23760: "Total",
    23761: "Total"
};

const totalGiftText = document.getElementById("text_gift_total_send");

if (totalGiftTextMap && totalGiftTextMap[stepper_id]) {
    totalGiftText.textContent = totalGiftTextMap[stepper_id];
}


var form = document.getElementById('guestbook_form');
if (form) {
    var nameInput = form.querySelector('input[name="name"]');
    if (stepper_id == 23432) {
        if (nameInput && nameInput.value) {
            nameInput.value = '';
            nameInput.removeAttribute('readonly');
        }
    }
}

if (stepper_id == 22649) {

    const newTitle = document.createElement('h3');
    newTitle.textContent = couple; // Change this text to your desired title
    newTitle.className = 'text-center text-dark mb-4'; // Add your desired classes here

    // Get the reference elements
    const rsvpCard = document.getElementById('rsvp_card');
    const rowElement = rsvpCard.querySelector('.row');

    // Insert the new title between rsvp_card and the row
    rsvpCard.insertBefore(newTitle, rowElement);

}
const form_rsvp = document.querySelector("#tambahdata");
if (form_rsvp && stepper_id == 23635) {
    const jumlahInput = form_rsvp.querySelector("input[name='jumlah']");
    if (jumlahInput) {
        jumlahInput.value = 2;
        jumlahInput.readOnly = true;
        jumlahInput.type = "hidden";
    }
    const jumlahSelect = form_rsvp.querySelector("select[name='jumlah']");
    if (jumlahSelect) {
        jumlahSelect.innerHTML = '<option value="2" selected hidden>2</option>';
        jumlahSelect.value = 2;
        jumlahSelect.style.display = "none";
    }
}


// Add this JavaScript code
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formGift');
    if (form) {
        const amountInput = form.querySelector('input[name="payment"]');
        const currencyEl = amountInput?.previousElementSibling;
        const regionMetadata = document.querySelector("meta[name='region_id']");
        const regionId = regionMetadata ? parseInt(regionMetadata.getAttribute("content")) : 1;

        try {
            if (currencyEl) {
                if (regionId === 2) {
                    currencyEl.textContent = "RM"
                } else {
                    currencyEl.textContent = "Rp"
                }
            }
        } catch (error) {
            console.error(error)
        }

        // Change input type from number to text to support formatting and selection
        amountInput.type = 'text';
        amountInput.inputMode = 'numeric'; // Show numeric keyboard on mobile

        // Remove the original validation attributes and add to our hidden field
        const minValue = amountInput.getAttribute('min');
        const maxValue = amountInput.getAttribute('max');
        const isRequired = amountInput.hasAttribute('required');

        // Create a hidden input to store the actual numeric value
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'payment';
        hiddenInput.value = amountInput.value;

        // Transfer validation attributes to hidden input
        if (minValue) hiddenInput.setAttribute('min', minValue);
        if (maxValue) hiddenInput.setAttribute('max', maxValue);
        if (isRequired) hiddenInput.setAttribute('required', 'required');

        // Rename the original input
        amountInput.name = 'payment_display';
        // Remove validation attributes from display input
        amountInput.removeAttribute('min');
        amountInput.removeAttribute('max');
        // amountInput.removeAttribute('required');

        // Insert the hidden input after the display input
        amountInput.parentNode.insertBefore(hiddenInput, amountInput.nextSibling);

        // Function to format number with thousand separators
        function formatNumber(number) {
            if (!number) return '';
            return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        }

        // Function to remove formatting and get raw number
        function removeFormatting(formattedNumber) {
            if (!formattedNumber) return '';
            return formattedNumber.toString().replace(/\./g, '');
        }

        // Function to validate if number exceeds maximum
        function validateMaxValue(rawValue) {
            if (!rawValue) return true;
            const numericValue = parseInt(rawValue);
            return !isNaN(numericValue) && numericValue <= 100000000;
        }

        // Function to validate if number meets minimum
        function validateMinValue(rawValue) {
            if (!rawValue) return true;
            const minValue = regionId === 2 ? 1 : 10000;
            const numericValue = parseInt(rawValue);
            return !isNaN(numericValue) && numericValue >= minValue;
        }

        // Custom validation for the display field
        function validateDisplayField() {
            const rawValue = removeFormatting(amountInput.value).replace(/\D/g, '');
            let isValid = true;
            let errorMessage = '';

            if (!rawValue && isRequired) {
                isValid = false;
                errorMessage = 'This field is required.';
            } else if (rawValue) {
                const numericValue = parseInt(rawValue);
                if (isNaN(numericValue)) {
                    isValid = false;
                    errorMessage = 'Please enter a valid number.';
                } else if (numericValue < 10000) {
                    isValid = false;
                    errorMessage = 'Amount must be at least Rp 10,000.';
                } else if (numericValue > 100000000) {
                    isValid = false;
                    errorMessage = 'Amount cannot exceed Rp 100,000,000.';
                }
            }

            // Update hidden input value
            hiddenInput.value = rawValue;

            // Manually trigger validation on hidden input
            if (window.jQuery && form.id) {
                const $form = $('#' + form.id);
                if ($form.data('validator')) {
                    $form.validate().element(hiddenInput);
                }
            }

            return { isValid, errorMessage };
        }

        // Handle input event for formatting
        amountInput.addEventListener('input', function (e) {
            // Get cursor position before formatting
            const cursorPosition = e.target.selectionStart;
            const originalValue = e.target.value;

            amountInput.classList.remove("is-invalid");

            // Remove any existing formatting and non-digit characters
            const rawValue = removeFormatting(originalValue).replace(/\D/g, '');

            // Check if value exceeds maximum
            if (rawValue && !validateMaxValue(rawValue)) {
                // If exceeds maximum, set to maximum value
                const maxValue = '100000000';
                e.target.value = formatNumber(maxValue);
                hiddenInput.value = maxValue;

                // Set cursor to end
                setTimeout(() => {
                    e.target.setSelectionRange(e.target.value.length, e.target.value.length);
                }, 0);

                // Trigger validation
                validateDisplayField();
                return;
            }

            // Update hidden input with raw value
            hiddenInput.value = rawValue;

            // Format the display value
            if (rawValue) {
                const formattedValue = formatNumber(rawValue);
                e.target.value = formattedValue;

                // Adjust cursor position after formatting
                setTimeout(() => {
                    // Calculate new cursor position
                    let newCursorPosition = cursorPosition;

                    // Count dots that were added before the original cursor position
                    const valueBeforeCursor = originalValue.substring(0, cursorPosition);
                    const rawBeforeCursor = removeFormatting(valueBeforeCursor).replace(/\D/g, '');
                    const formattedBeforeCursor = formatNumber(rawBeforeCursor);

                    newCursorPosition = formattedBeforeCursor.length;
                    e.target.setSelectionRange(newCursorPosition, newCursorPosition);
                }, 0);
            } else {
                e.target.value = '';
                hiddenInput.value = '';
            }

            // Trigger validation
            validateDisplayField();
        });

        // Handle focus event - remove formatting for editing
        amountInput.addEventListener('focus', function (e) {
            const formattedValue = e.target.value;
            if (formattedValue) {
                const rawValue = removeFormatting(formattedValue);
                e.target.value = rawValue;

                // Set cursor to end when focusing
                setTimeout(() => {
                    e.target.setSelectionRange(rawValue.length, rawValue.length);
                }, 0);
            }
        });

        // Handle blur event - add formatting when leaving the field
        amountInput.addEventListener('blur', function (e) {
            const rawValue = removeFormatting(e.target.value).replace(/\D/g, '');

            if (rawValue) {
                // Validate min and max values
                if (!validateMinValue(rawValue)) {
                    e.target.value = formatNumber('10000');
                    hiddenInput.value = '10000';
                } else if (!validateMaxValue(rawValue)) {
                    e.target.value = formatNumber('100000000');
                    hiddenInput.value = '100000000';
                } else {
                    e.target.value = formatNumber(rawValue);
                    hiddenInput.value = rawValue;
                }
            } else {
                e.target.value = '';
                hiddenInput.value = '';
            }

            // Trigger validation
            validateDisplayField();
        });

        // Handle keydown to restrict input to numbers only
        amountInput.addEventListener('keydown', function (e) {
            // Allow: backspace, delete, tab, escape, enter, arrows
            if ([46, 8, 9, 27, 13, 110, 190].includes(e.keyCode) ||
                // Allow: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true) ||
                // Allow: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)) {
                return;
            }

            // Ensure that it is a number and stop the keypress if not
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }

            // Get current raw value
            const currentRawValue = removeFormatting(e.target.value).replace(/\D/g, '');

            // Prevent typing if already at max length (9 digits for 100,000,000)
            if (currentRawValue.length >= 9 &&
                e.keyCode >= 48 && e.keyCode <= 57 ||
                e.keyCode >= 96 && e.keyCode <= 105) {
                e.preventDefault();
            }
        });

        // Handle paste event to clean pasted content
        amountInput.addEventListener('paste', function (e) {
            e.preventDefault();
            const pastedText = (e.clipboardData || window.clipboardData).getData('text');
            const numbersOnly = pastedText.replace(/\D/g, '');

            // Insert the cleaned numbers at cursor position
            const startPos = e.target.selectionStart;
            const endPos = e.target.selectionEnd;
            const currentValue = removeFormatting(e.target.value).replace(/\D/g, '');

            const newValue = currentValue.substring(0, startPos) + numbersOnly + currentValue.substring(endPos);

            // Validate max length
            const finalValue = newValue.substring(0, 9); // Max 9 digits

            // Update the input
            e.target.value = finalValue;
            hiddenInput.value = finalValue;

            // Trigger input event to format
            e.target.dispatchEvent(new Event('input'));
        });

        // Override jQuery Validation for our custom field
        if (window.jQuery) {
            $(document).ready(function () {
                // Remove any existing validation for payment_display
                // if ($('#formGift').data('validator')) {
                //     const validator = $('#formGift').validate();
                //     if (validator.settings.rules.payment_display) {
                //         delete validator.settings.rules.payment_display;
                //     }
                // }

                // Add custom validation method if needed
                $.validator.addMethod('paymentRange', function (value, element) {
                    const rawValue = removeFormatting(value).replace(/\D/g, '');
                    if (!rawValue) return true; // Let required handle empty

                    const numericValue = parseInt(rawValue);
                    return !isNaN(numericValue) && numericValue >= 10000 && numericValue <= 100000000;
                }, 'Amount must be between Rp 10,000 and Rp 100,000,000');

                $.validator.addMethod('paymentRequired', function (value, element) {
                    const rawValue = removeFormatting(value).replace(/\D/g, '');
                    return rawValue.length > 0; // wajib ada angka
                }, 'This field required');
            });
        }

        // Handle form submission to ensure hidden input has the correct value
        form.addEventListener('submit', function (e) {
            // Ensure the hidden input has the latest raw value
            const displayValue = amountInput.value;
            if(!displayValue){
                e.preventDefault();
                amountInput.classList.add('is-invalid');
                return;
            }
            const rawValue = removeFormatting(displayValue).replace(/\D/g, '');

            // Final validation before submission
            if (rawValue) {
                if (!validateMinValue(rawValue)) {
                    hiddenInput.value = '10000';
                } else if (!validateMaxValue(rawValue)) {
                    hiddenInput.value = '100000000';
                } else {
                    hiddenInput.value = rawValue;
                }
            } else {
                hiddenInput.value = '';
            }

            // Trigger final validation
            validateDisplayField();
        });

        // Initialize with current value if any
        if (amountInput.value) {
            const rawValue = removeFormatting(amountInput.value).replace(/\D/g, '');
            if (validateMinValue(rawValue) && validateMaxValue(rawValue)) {
                hiddenInput.value = rawValue;
                amountInput.value = formatNumber(rawValue);
            } else if (rawValue && !validateMinValue(rawValue)) {
                hiddenInput.value = '10000';
                amountInput.value = formatNumber('10000');
            } else if (rawValue && !validateMaxValue(rawValue)) {
                hiddenInput.value = '100000000';
                amountInput.value = formatNumber('100000000');
            }
        }

        // Initial validation
        setTimeout(validateDisplayField, 100);
    }
});

if (stepper_id == 25114) {
    const url = new URL(window.location.href);
    const name = url.searchParams.get("name");
    if (name) {
        const newInput = document.createElement("input");
        newInput.classList.add("form-control", "mb-3");
        newInput.name = "jumlah";
        newInput.type = "number";
        newInput.maxLength = 3;
        newInput.max = 100;

        const select = document.querySelector(".rsvp-section form select[name='jumlah']");
        if (select) {
            select.replaceWith(newInput);
        }
    }
}

// change theme
// function changeTheme() {
//     fetch('/test-theme')
//         .then(response => response.json())
//         .then(data => {
//             console.log('API response:', data);
//             location.reload()
//         })
//         .catch(error => {
//             console.error('Error calling the API:', error);
//             location.reload()
//         });

// }
// setInterval(changeTheme, 10000)

function normalizeTimeString(str) {
    return str.replace(
        /^(\d{1,2}:\d{2})\s*-\s*(Selesai|End)\s+(WIB|WITA|WIT)$/i,
        '$1 $3 - $2'
    );
}

function containsTime(str) {
  const regex = /\b([01]?\d|2[0-3]):[0-5]\d\b/;
  return regex.test(str);
}


try {
    if(stepper_id !== 25652){
        const events = document.querySelectorAll(".venue-section .venue-content .card");
        events.forEach(event=>{
            const pTag = event.querySelectorAll(".event-name p");
    
            pTag.forEach(p=>{
                if(containsTime(p.textContent.trim())){
                    p.textContent = normalizeTimeString(p.textContent.trim());
                }
            })
        });
    }
} catch (error) {
    console.error(error)
}

const inputWishes = document.querySelectorAll("form#guestbook_form input[name='name'], form#guestbook_form input[name='alamat'], form#guestbook_form textarea[name='comment']");
inputWishes.forEach(input=>{
    input.required = true;
});
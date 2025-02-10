document.addEventListener('DOMContentLoaded', () => {

    const predictForm = document.getElementById('predictForm');
    const reportForm = document.getElementById('reportForm');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
   

    if (predictForm) {
        predictForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(predictForm);
            const data = Object.fromEntries(formData);
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            document.getElementById('message').innerText = result.message + (result.prediction_id ? ` Prediction ID: ${result.prediction_id}` : '');
        });
    }

    if (reportForm) {
        reportForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(reportForm);
            const data = Object.fromEntries(formData);
            const response = await fetch('/report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            document.getElementById('message').innerText = result.message;
        });
    }

    // Translation functionality
    const translations = {
        en: {
            home: 'Home',
            login: 'Login',
            predict: 'Predict',
            report: 'Report',
            welcome: 'Welcome to AgriProphets',
            intro: 'Your one-stop solution for accurate agricultural predictions and reports.',
            username: 'Username',
            password: 'Password',
            registerButton: 'Register Here',
            name: 'Name',
            email: 'Email',
            location: 'Location',
            phone: 'Phone Number',
            confirmPassword: 'Confirm Password',
            register: 'Register',
        },
        hi: {
            home: 'होम',
            login: 'लॉगिन',
            predict: 'भविष्यवाणी',
            report: 'रिपोर्ट',
            welcome: 'अग्रिप्रोफेट्स में आपका स्वागत है',
            intro: 'सटीक कृषि पूर्वानुमान और रिपोर्ट के लिए आपका एकमात्र समाधान।',
            username: 'उपयोगकर्ता नाम',
            password: 'पासवर्ड',
            registerButton: 'पंजीकृत करें',
            name: 'नाम',
            email: 'ईमेल',
            location: 'स्थान',
            phone: 'फोन नंबर',
            confirmPassword: 'पासवर्ड की पुष्टि करें',
            register: 'पंजीकृत' ,
        },
        bn: {
            home: 'হোম',
            login: 'লগইন',
            predict: 'ভবিষ্যদ্বাণী',
            report: 'রিপোর্ট',
            welcome: 'অ্যাগ্রি প্রফেটসে আপনাকে স্বাগতম',
            intro: 'সঠিক কৃষি পূর্বাভাস এবং প্রতিবেদন জন্য আপনার একক সমাধান।',
            username: 'ব্যবহারকারীর নাম',
            password: 'পাসওয়ার্ড',
            registerButton: 'নিবন্ধন করুন',
            name: 'নাম',
            email: 'ইমেইল',
            location: 'অবস্থান',
            phone: 'ফোন নম্বর',
            confirmPassword: 'পাসওয়ার্ড নিশ্চিত করুন',
            register: 'নিবন্ধন' ,
        },
        ta: {
            home: 'முகப்பு',
            login: 'உள்நுழைக',
            predict: 'பரிசீலனை',
            report: 'அறிக்கை',
            welcome: 'அக்ரிப்ரொப்ஷெட் உங்கள் வரவேற்பு',
            intro: 'சரியான விவசாய முன்னறிவிப்பு மற்றும் அறிக்கைகளுக்கான உங்கள் ஒரே நிலைத் தீர்வு.',
            username: 'பயனர் பெயர்',
            password: 'கடவுச்சொல்',
            registerButton: 'பதிவு செய்யவும்',
            name: 'பெயர்',
            email: 'மின்னஞ்சல்',
            location: 'இடம்',
            phone: 'தொலைபேசி எண்',
            confirmPassword: 'கடவுச்சொல்லை உறுதிசெய்க',
            register: 'பதிவு',
        },
        te: {
            home: 'హోమ్',
            login: 'లాగిన్',
            predict: 'అంచనా',
            report: 'రిపోర్ట్',
            welcome: 'అగ్రిప్రొఫెట్లకు స్వాగతం',
            intro: 'సరిగ్గా వ్యవసాయ అంచనాలు మరియు నివేదికల కోసం మీ ఒక్కటే పరిష్కారం.',
            username: 'ఉపయోగదారు పేరు',
            password: 'పాస్వర్డ్',
            registerButton: 'నమోదు చేయండి',
            name: 'పేరు',
            email: 'ఇమెయిల్',
            location: 'స్థానం',
            phone: 'ఫోన్ నంబర్',
            confirmPassword: 'పాస్వర్డ్ను ధృవీకరించండి',
            register: 'నమోదు',
        },
        kn: {
            home: 'ಮನೆ',
            login: 'ಲಾಗಿನ್',
            predict: 'ಭವಿಷ್ಯವಾಣಿ',
            report: 'ಅಹवालು',
            welcome: 'ಅಗ್ರಿಪ್ರೊಫೆಟ್ಸ್ ಗೆ ಸ್ವಾಗತ',
            intro: 'ತ Accurate ಕೃಷಿ ಮುನ್ಸೂಚನೆ ಮತ್ತು ವರದಿಗಳಿಗಾಗಿ ನಿಮ್ಮ ಒಬ್ಬೋ ಪರಿಹಾರ.',
            username: 'ಬಳಕೆದಾರ ಹೆಸರು',
            password: 'ಪಾಸ್ವರ್ಡ್',
            registerButton: 'ನೊಂದಣಿ',
            name: 'ಹೆಸರು',
            email: 'ಇಮೇಲ್',
            location: 'ಸ್ಥಳ',
            phone: 'ದೂರವಾಣಿ ಸಂಖ್ಯೆ',
            confirmPassword: 'ಪಾಸ್ವರ್ಡ್ ದೃಢೀಕರಿಸಿ',
            register: 'ನೋಂದಣಿ',
        },
        gu: {
            home: 'મુખ્ય પાનું',
            login: 'લોગિન',
            predict: 'અગાઉનો અંદાજ',
            report: 'અહેવાલ',
            welcome: 'એગ્રીપ્રોફેટ્સમાં આપનું સ્વાગત છે',
            intro: 'સચોટ કૃષિ આગાહીઓ અને અહેવાલો માટે તમારું એકમાત્ર ઉકેલ.',
            username: 'વપરાશકર્તાનું નામ',
            password: 'પાસવર્ડ',
            registerButton: 'નોંધણી કરો',
            name: 'નામ',
            email: 'ઇમેઇલ',
            location: 'સ્થાન',
            phone: 'ફોન નંબર',
            confirmPassword: 'પાસવર્ડની પુષ્ટિ કરો',
            register: 'નોંધણી',
        }
    };

    const languageSelect = document.getElementById('languageSelect');
    languageSelect.addEventListener('change', () => {
        const selectedLanguage = languageSelect.value;
        applyTranslations(selectedLanguage);
    });

    function applyTranslations(language) {
        const elementsToTranslate = document.querySelectorAll('[data-translate-key]');
        elementsToTranslate.forEach(el => {
            const key = el.getAttribute('data-translate-key');
            if (translations[language] && translations[language][key]) {
                el.textContent = translations[language][key];
            }
        });
    }

    // Initialize translations on page load
    applyTranslations(languageSelect.value || 'en');
});



document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.querySelector('#registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            
            const formData = new FormData(registerForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                alert(result.message); // Show the message
                if (response.ok) {
                    // Optional redirection after registration
                    window.location.href = '/login'; 
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }

    const loginForm = document.querySelector('#loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                alert(result.message); // Show the message
                if (response.ok) {
                    // Redirect to the predict page
                    window.location.href = result.redirect;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }
});

export async function loginGetToken(email, password){
    try {
        const response = await fetch('api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email, password})
        });

        if (response.status === 429) {
            // Handle too many attempts
            const error = await response.json();
            throw new Error(error.detail); // "Too many failed attempts. Please try again in 15 minutes"
        }

        await validateResponse(response);
        const data = await response.json();
        return data.access_token;
    } catch (error) {
    // Extract remaining attempts from error message if available
        if (error.message.includes('attempts remaining')) {
            const remainingAttempts = error.message.match(/(\d+) attempts remaining/)[1];
            error.remainingAttempts = parseInt(remainingAttempts);
        }
        throw error;
    }
}

export async function validateResponse(response) {
    if (!response.ok) {
        if (response.json) {
            const error = await response.json();
            if (error.non_field_errors) {
                throw new Error(error.non_field_errors[0]);
            }
            if (error.password) {
                throw new Error(error.password.join(' '))
            }
            if (error.email) {
                throw new Error(error.email.join(' '))
            }
            if (error.username) {
                throw new Error(error.username.join(' '))
            }
            if (error.video) {
                throw new Error(error.password.join(' '))
            }
            if (error.text) {
                throw new Error(error.text.join(' '))
            }
            if (error.title) {
                throw new Error(error.title.join(' '))
            }
            throw new Error(error.detail);
        }
        throw new Error(response.statusText);
    }
}

export async function registerUser(login, password, email){
    const response = await fetch('api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
             username,
             email,
             password,
             confirm_password: password
        })
    });
    await validateResponse(response);
    return await response.json();
}

export async function logout(token){
    const response = await fetch('api/auth/logout', {
        method: 'POST',
    });
    await validateResponse(response);
}

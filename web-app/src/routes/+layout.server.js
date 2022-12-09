 export const load = ({ locals }) => {
    if (locals.user) {
        return {
            user: locals.user
        }
    } else {
        return {
            user: undefined
        }
    }
 }
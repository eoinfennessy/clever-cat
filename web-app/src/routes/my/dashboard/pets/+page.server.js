import { error } from "@sveltejs/kit"
import { serialiseNonPojos } from '$lib/utils'

export const load = ({ locals }) => {
    if (!locals.pb.authStore.isValid) {
        throw redirect(303, '/login')
    }
    
    const getPets = async () => {
        try {
            const pets = serialiseNonPojos(await locals.pb.collection('pets').getFullList(200, {filter: `user = "${locals.user.id}"`}));
            console.log(pets)
            return pets
        } catch (err) {
            console.log('Error: ', err);
            throw error(err.status, err.message);
        }
    }

    return {
        pets: getPets()
    }
}
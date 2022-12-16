import { serialiseNonPojos } from '$lib/utils'
import { error } from '@sveltejs/kit'

export const load = ({ locals, params }) => {
    const getPet = async (petId) => {
        try {
            const feeder = serialiseNonPojos(await locals.pb.collection('pets').getOne(petId))
            console.log(feeder)
            return feeder
        } catch (err) {
            console.log('Error: ', err);
            throw error(err.status, err.message);
        }
    }
    return {
        pet: getPet(params.petId)
    }
}
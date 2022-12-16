import { error } from "@sveltejs/kit"
import { serialiseNonPojos } from '$lib/utils'

export const load = ({ locals }) => {
    if (!locals.pb.authStore.isValid) {
        throw redirect(303, '/login')
    }
    
    const getFeeders = async () => {
        try {
            const feeders = serialiseNonPojos(await locals.pb.collection('feeders').getFullList(200, {filter: `user = "${locals.user.id}"`}));
            // const feeders = serialiseNonPojos(await locals.pb.collection('feeders').getFullList(200, {filter: `user = "${locals.user.id}"`, expand: 'model.pet'}));
            console.log(feeders)
            return feeders
        } catch (err) {
            console.log('Error: ', err);
            throw error(err.status, err.message);
        }
    }

    return {
        feeders: getFeeders()
    }
}
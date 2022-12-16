import { serialiseNonPojos } from '$lib/utils'
import { error } from '@sveltejs/kit'

export const load = ({ locals, params }) => {
    const getFeeder = async (feederId) => {
        try {
            const feeder = serialiseNonPojos(await locals.pb.collection('feeders').getOne(feederId, {expand: 'model'}))
            console.log(feeder)
            return feeder
        } catch (err) {
            console.log('Error: ', err);
            throw error(err.status, err.message);
        }
    }
    return {
        feeder: getFeeder(params.feederId)
    }
}
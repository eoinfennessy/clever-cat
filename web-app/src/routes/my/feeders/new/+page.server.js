import { error, redirect } from "@sveltejs/kit";

export const load = ({ locals }) => {
    if (!locals.pb.authStore.isValid) {
        throw redirect(303, '/login')
    }
}

export const actions = {
  create: async ({ request, locals }) => {
    const body = await request.formData();
    
    const thumbnail = body.get('thumbnail');
    if (!thumbnail.size) {
      body.delete('thumbnail');
    }

    body.append('user', locals.user.id)
    // Default Model
    body.append('model', '7hyusgq7gp56ltp')

    try {
      await locals.pb.collection("feeders").create(body);
    } catch (err) {
      console.log("Error: ", err);
      throw error(err.status, err.message);
    }

    throw redirect(303, '/')
  },
};
import { error, redirect } from "@sveltejs/kit";

export const load = ({ locals }) => {
    if (!locals.pb.authStore.isValid) {
        throw redirect(303, '/login')
    }
}

export const actions = {
  create: async ({ request, locals }) => {
    const body = await request.formData();
    
    const avatar = body.get('avatar');
    if (!avatar.size) {
      body.delete('avatar');
    }

    body.append('user', locals.user.id)

    try {
      await locals.pb.collection("pets").create(body);
    } catch (err) {
      console.log("Error: ", err);
      throw error(err.status, err.message);
    }

    throw redirect(303, '/')
  },
};
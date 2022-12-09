import { error } from "@sveltejs/kit";

export const actions = {
  updateProfile: async ({ request, locals }) => {
    const body = await request.formData();
    const userAvatar = body.get('avatar');

    if (!userAvatar.size) {
      body.delete('avatar');
    }

    try {
      const { name, avatar } = await locals.pb.collection("users").update(locals?.user?.id, body);
      locals.user.name = name;
      locals.user.avatar = avatar;
    } catch (err) {
      console.log("Error: ", err);
      throw error(400, "Something went wrong when updating your profile");
    }
    return {
      success: true,
    };
  },
};

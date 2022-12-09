import { error } from "@sveltejs/kit";

export const actions = {
  updateEmail: async ({ request, locals }) => {
    const body = Object.fromEntries(await request.formData());

    try {
      await locals.pb.collection("users").requestEmailChange(body.email);
    } catch (err) {
      console.log("Error: ", err);
      throw error(err.status, "Something went wrong when updating email");
    }

    return {
      success: true,
    };
  },

  updateUsername: async ({ request, locals }) => {
    const body = Object.fromEntries(await request.formData());

    try {
      await locals.pb.collection("users").getFirstListItem(`username = "${body.username}"`);
    } catch (err) {
      // If no record with that username already exists
      if (err.status === 404) {
        try {
          const { username } = await locals.pb.collection('users').update(locals.user.id, { username: body.username });
          locals.user.username = username;
          return {
            success: true,
          };
        } catch (err) {
          console.log("Error: ", err);
          throw error(err.status, "Something went wrong when updating username");
        }
      } else {
        console.log("Error: ", err);
        throw error(err.status, "Something went wrong when updating username");
      }
    }
    console.log("Error: ", `Username ${body.username} already exists in DB`);
    return {
      success: false,
    };
  },
};

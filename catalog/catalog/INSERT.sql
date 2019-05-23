INSERT INTO public.user (id, name, email, picture) VALUES ('1', 'Robo Barista', 'tinnyTim@udacity.com', '');

INSERT INTO public.category (id, name, user_id) VALUES ('1', 'Soccer', '1');
INSERT INTO public.category (id, name, user_id) VALUES ('2', 'Basketball', '1');
INSERT INTO public.category (id, name, user_id) VALUES ('3', 'Baseball', '1');
INSERT INTO public.category (id, name, user_id) VALUES ('4', 'Frisbee', '1');
INSERT INTO public.category (id, name, user_id) VALUES ('5', 'Snowboarding', '1');
INSERT INTO public.category (id, name, user_id) VALUES ('6', 'Rock Climbing', '1');

INSERT INTO public.item (id, category_id, title, description, user_id) VALUES ('1', '1', 'Soccer cleats', 'The shoes', '1');
INSERT INTO public.item (id, category_id, title, description, user_id) VALUES ('2', '1', 'Jersey', 'The shirt', '1');
INSERT INTO public.item (id, category_id, title, description, user_id) VALUES ('3', '3', 'Bat', 'The bat', '1');
INSERT INTO public.item (id, category_id, title, description, user_id) VALUES ('4', '5', 'Snowboard', 'Best for any terrain and conditions. All-mountain snowboards perform anywhere on a mountain-groomed run, backcountry, even park and pipe. They may be directional (meaning downhill only) or twin-tip (for riding switch, meaning either direction). Most boarders ride all-mountain boards. Because of the versatility, all-mountain boards are good for beginners who are still learning what terrain they like.', '1');

CREATE TABLE IF NOT EXISTS public.menu
(
    id integer NOT NULL DEFAULT nextval('menu_id_seq'::regclass),
    named character varying(255) COLLATE pg_catalog."default",
    types character varying(255) COLLATE pg_catalog."default",
    cost integer NOT NULL,
    CONSTRAINT menu_pkey PRIMARY KEY (id),
    CONSTRAINT menu_id_unique UNIQUE (id)
);
CREATE TABLE IF NOT EXISTS public.orders
(
    id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
    created_date date NOT NULL,
    updated_date date NOT NULL,
    address character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT orders_pkey PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS order_products (
    id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
    order_id integer,
    menu_id integer,
    CONSTRAINT order_products_pkey PRIMARY KEY (id),
    CONSTRAINT order_products_menu_id_fkey FOREIGN KEY (menu_id)
        REFERENCES public.menu (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT order_products_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES public.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS public.order_messages
(
    id integer NOT NULL DEFAULT nextval('order_products_id_seq'::regclass),
    order_id integer,
    assistant_messages character varying(1000) COLLATE pg_catalog."default",
    user_messages character varying(1000) COLLATE pg_catalog."default",
    CONSTRAINT order_messages_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES public.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
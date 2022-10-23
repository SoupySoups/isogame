from moderngl_window.context.base import WindowConfig
from moderngl_window.timers.clock import Timer
from moderngl_window import (
    create_parser,
    parse_args,
    get_local_window_cls,
    activate_context,
)
import pygame
import moderngl
from moderngl_window import geometry
from logging import ERROR
from pathlib import Path


class window(WindowConfig):
    log_level = ERROR
    resource_dir = (
        Path(__file__) / "./../../"
    ).absolute()  # Where the search for resources begins

    def __init__(self, window_size, title, render_size) -> None:
        self.window_size = window_size
        self.title = title
        self.render_size = render_size

        self.screen = pygame.Surface(self.render_size, flags=pygame.SRCALPHA)

        self.parser = create_parser()
        self.add_arguments(self.parser)
        self.values = parse_args(args=("--window", "pygame2"), parser=self.parser)
        self.argv = self.values
        self.window_cls = get_local_window_cls(self.values.window)

        self.window_size = (
            int(self.window_size[0] * self.values.size_mult),
            int(self.window_size[1] * self.values.size_mult),
        )

        # Resolve cursor
        self.show_cursor = True
        self.fullscreen = False
        self.resizable = True
        self.vsync = True

        self.window = self.window_cls(
            title=self.title,
            size=self.window_size,
            fullscreen=self.fullscreen,
            resizable=self.resizable,
            gl_version=self.gl_version,
            aspect_ratio=self.aspect_ratio,
            vsync=self.vsync,
            samples=self.samples,
            cursor=self.show_cursor,
        )
        self.window.process_events = lambda: None
        self.window.exit_key = None
        activate_context(window=self.window)
        self.timer = Timer()

        super().__init__(ctx=self.window.ctx, wnd=self.window, timer=self.timer)

        self.pg_texture = self.ctx.texture(self.render_size, 4)
        self.pg_texture.filter = moderngl.NEAREST, moderngl.NEAREST

        self.programs = []
        self.loadShader()

        self.quad_fs = geometry.quad_fs()

        self.window.swap_buffers()
        self.window.set_default_viewport()

        self.timer.start()

    def loadShader(self, frag=None, vert=None, raw=False):
        if not raw:
            if frag is not None:
                with open(frag) as f:
                    frag = f.read()
            else:
                frag = """
#version 330
// Vertex Shader

out vec4 fragColor;
uniform sampler2D texture0;
in vec2 uv0;

void main() {
    fragColor = texture(texture0, uv0);
}
"""
            if vert is not None:
                with open(vert) as f:
                    vert = f.read()
            else:
                vert = """
#version 330
// Vertex Shader

in vec3 in_position;
in vec2 in_texcoord_0;
out vec2 uv0;

void main() {
    gl_Position = vec4(in_position, 1);
    uv0 = in_texcoord_0;
}
"""
        self.programs.append(self.ctx.program(vertex_shader=vert, fragment_shader=frag))
        return self.programs[-1]

    def removeShader(self, shader):
        self.programs.remove(shader)

    @property
    def running(self):
        return not self.window.is_closing

    def render(self, current_time, delta):
        pass

    def update(self):
        # texture_data = pygame.transform.flip(self.screen, False, True).get_view("1")
        texture_data = pygame.image.tostring(self.screen, "RGBA", True)

        self.pg_texture.write(texture_data)

        self.ctx.clear(0, 0, 0)

        self.ctx.enable(moderngl.BLEND)
        self.pg_texture.use()
        for prog in self.programs:
            self.quad_fs.render(prog)
        self.ctx.disable(moderngl.BLEND)

        current_time, delta = self.timer.next_frame()

        self.window.use()

        self.window.render(current_time, delta)
        if not self.window.is_closing:
            self.window.swap_buffers()

        return (current_time, delta)

    def close(self):
        self.window.destroy()

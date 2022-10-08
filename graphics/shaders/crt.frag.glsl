#version 330
// Frag shader

out vec4 fragColor;
uniform sampler2D texture0;
in vec2 uv0;

void main() {
    vec2 center = vec2(0.5, 0.5);
    vec2 off_center = uv0 - center;

    off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(2.5));

    vec2 v_text2 = center+off_center;

    fragColor = vec4(texture(texture0, v_text2).rgb, 1.0);

    if (v_text2.x > 1.0 || v_text2.x < 0.0 ||
      v_text2.y > 1.0 || v_text2.y < 0.0){
    fragColor=vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        fragColor = vec4(texture(texture0, v_text2).rgb, 1.0);
        float fv = fract(v_text2.y * float(textureSize(texture0,0).y));
        fv=min(1.0, 0.8+0.5*min(fv, 1.0-fv));
        fragColor.rgb*=fv;
    }
}

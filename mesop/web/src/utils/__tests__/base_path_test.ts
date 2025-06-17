import {test} from 'node:test';
import assert from 'node:assert';

import {prefixBasePath} from '../base_path';

test('returns original path when no base is set', () => {
  global.window = {};
  assert.strictEqual(prefixBasePath('/foo'), '/foo');
});

test('adds base path to absolute path', () => {
  global.window = {__MESOP_BASE_URL_PATH__: '/base'};
  assert.strictEqual(prefixBasePath('/foo'), '/base/foo');
});

test('adds base path to relative path', () => {
  global.window = {__MESOP_BASE_URL_PATH__: '/base'};
  assert.strictEqual(prefixBasePath('foo'), '/base/foo');
});

test('handles base path ending with slash', () => {
  global.window = {__MESOP_BASE_URL_PATH__: '/base/'};
  assert.strictEqual(prefixBasePath('/foo'), '/base/foo');
});
